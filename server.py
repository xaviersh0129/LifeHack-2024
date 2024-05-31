import os
import aiohttp
from quart import Quart, request, jsonify
from quart_cors import cors
import asyncio
import geojson
import ssl
import certifi
from bs4 import BeautifulSoup
from dotenv import load_dotenv

app = Quart(__name__)
app = cors(app)

load_dotenv()
api_key = os.getenv('API_KEY')

geojson_file_path = 'Datasets/singapore_with_police_stations.geojson'
with open(geojson_file_path, 'r') as f:
    geojson_data = geojson.load(f)

def extract_name(description):
    soup = BeautifulSoup(description, 'html.parser')
    rows = soup.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        if cells and 'DIVISION' in cells[0].text:
            return cells[1].text.strip()
    return 'Unknown'

police_stations = []
for feature in geojson_data['features']:
    if feature['geometry']['type'] == 'Point':
        coordinates = feature['geometry']['coordinates']
        description = feature['properties'].get('Description', '')
        name = extract_name(description)
        police_stations.append((coordinates[1], coordinates[0], name))

def chunk_list(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

async def get_travel_times(session, api_key, origin, destinations):
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json'
    destinations_str = '|'.join([f"{lat},{lon}" for lat, lon, _ in destinations])
    params = {
        'origins': f"{origin[0]},{origin[1]}",
        'destinations': destinations_str,
        'key': api_key,
        'mode': 'driving'
    }
    async with session.get(url, params=params) as response:
        return await response.json()

async def get_coordinates(session, api_key, address):
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'address': address, 'key': api_key}
    async with session.get(url, params=params) as response:
        return await response.json()

async def get_address(session, api_key, lat, lon):
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'latlng': f"{lat},{lon}", 'key': api_key}
    async with session.get(url, params=params) as response:
        try:
            return await response.json()
        except aiohttp.ContentTypeError as e:
            text = await response.text()
            print(f"Failed to decode JSON. Response text: {text}")
            raise e

@app.route('/api/closest_stations', methods=['GET'])
async def get_closest_stations():
    address = request.args.get('address')
    if not address:
        return jsonify({'error': 'Address is required'}), 400

    ssl_context = ssl.create_default_context(cafile=certifi.where())

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
        address_response = await get_coordinates(session, api_key, address)
        if address_response['status'] != 'OK':
            return jsonify({'error': 'Error in Geocoding API request', 'details': address_response}), 500
        
        coordinates = address_response['results'][0]['geometry']['location']
        fixed_spot = (coordinates['lat'], coordinates['lng'])

        max_elements = 25
        chunks = list(chunk_list(police_stations, max_elements))

        tasks = [get_travel_times(session, api_key, fixed_spot, chunk) for chunk in chunks]
        responses = await asyncio.gather(*tasks)

    travel_times_list = []
    for response, chunk in zip(responses, chunks):
        if response['status'] == 'OK':
            for element, station in zip(response['rows'][0]['elements'], chunk):
                if element['status'] == 'OK':
                    duration = element['duration']['value']
                    travel_times_list.append((station, duration))
        else:
            return jsonify({'error': 'Error in the API request', 'details': response}), 500

    travel_times_list.sort(key=lambda x: x[1])
    top_3_travel_times = travel_times_list[:3]

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
        tasks = [get_address(session, api_key, lat, lon) for (lat, lon, name), _ in top_3_travel_times]
        try:
            address_responses = await asyncio.gather(*tasks)
        except aiohttp.ContentTypeError as e:
            return jsonify({'error': 'Failed to decode JSON response', 'details': str(e)}), 500

    results = []
    for idx, ((lat, lon, name), duration), address_response in zip(range(1, 4), top_3_travel_times, address_responses):
        address = address_response['results'][0]['formatted_address'] if address_response['status'] == 'OK' else 'Address not found'
        results.append({
            'name': name,
            'address': address,
            'travelTime': duration / 60
        })

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
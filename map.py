import aiohttp
import asyncio
import geojson
import ssl
import certifi
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('api_key')

# Load the GeoJSON file
with open('Datasets/singapore_with_police_stations.geojson', 'r') as f:
    geojson_data = geojson.load(f)

# Function to extract meaningful name from the Description field
def extract_name(description):
    soup = BeautifulSoup(description, 'html.parser')
    rows = soup.find_all('tr')
    for row in rows:
        if 'DIVISION' in row.text:
            return row.find_all('td')[1].text
    return None

# Extract police station coordinates and meaningful names
police_stations = []
for feature in geojson_data['features']:
    if feature['geometry']['type'] == 'Point':
        coordinates = feature['geometry']['coordinates']
        description = feature['properties'].get('Description', '')
        name = extract_name(description) if description else 'Unknown'
        police_stations.append((coordinates[1], coordinates[0], name))

# Function to chunk a list into smaller lists
def chunk_list(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

# Asynchronous function to make a request to the Distance Matrix API
async def get_travel_times(session, api_key, origin, destinations):
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json'
    destinations_str = '|'.join([f"{lat},{lon}" for lat, lon, _ in destinations])
    params = {
        'origins': f"{origin[0]},{origin[1]}",
        'destinations': destinations_str,
        'key': api_key,
        'mode': 'driving'  # You can change this to 'walking', 'bicycling', 'transit'
    }
    async with session.get(url, params=params) as response:
        return await response.json()

# Asynchronous function to make a request to the Geocoding API
async def get_coordinates(session, api_key, address):
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {
        'address': address,
        'key': api_key
    }
    async with session.get(url, params=params) as response:
        return await response.json()

# Asynchronous function to make a request to the Geocoding API for reverse geocoding
async def get_address(session, api_key, lat, lon):
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {
        'latlng': f"{lat},{lon}",
        'key': api_key
    }
    async with session.get(url, params=params) as response:
        return await response.json()

# Asynchronous main function to handle multiple requests
async def main():
    address = input("Enter the address: ")

    # Create SSL context to use certifi certificates
    ssl_context = ssl.create_default_context(cafile=certifi.where())

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
        # Get coordinates for the input address
        address_response = await get_coordinates(session, api_key, address)
        if address_response['status'] != 'OK':
            print("Error in Geocoding API request:", address_response['status'])
            if 'error_message' in address_response:
                print("Error message:", address_response['error_message'])
            return
        
        coordinates = address_response['results'][0]['geometry']['location']
        fixed_spot = (coordinates['lat'], coordinates['lng'])

        max_elements = 25  # Standard usage limit
        chunks = list(chunk_list(police_stations, max_elements))

        tasks = []
        for chunk in chunks:
            task = asyncio.ensure_future(get_travel_times(session, api_key, fixed_spot, chunk))
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks)

    travel_times_list = []
    for response, chunk in zip(responses, chunks):
        if response['status'] == 'OK':
            for element, station in zip(response['rows'][0]['elements'], chunk):
                if element['status'] == 'OK':
                    duration = element['duration']['value']  # Duration in seconds
                    travel_times_list.append((station, duration))
        else:
            print("Error in the API request:", response['status'])
            if 'error_message' in response:
                print("Error message:", response['error_message'])

    # Sort the travel times list by duration
    travel_times_list.sort(key=lambda x: x[1])

    # Get the top 3 shortest travel times
    top_3_travel_times = travel_times_list[:3]

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
        tasks = []
        for (lat, lon, name), _ in top_3_travel_times:
            task = asyncio.ensure_future(get_address(session, api_key, lat, lon))
            tasks.append(task)
        
        address_responses = await asyncio.gather(*tasks)

    # Print the top 3 closest police stations with their addresses
    for idx, ((lat, lon, name), duration), address_response in zip(range(1, 4), top_3_travel_times, address_responses):
        if address_response['status'] == 'OK':
            address = address_response['results'][0]['formatted_address']
        else:
            address = 'Address not found'
        print(f"{idx}. Police station at {address} with a travel time of {duration / 60:.2f} minutes.")

# Run the asynchronous main function
if __name__ == '__main__':
    asyncio.run(main())

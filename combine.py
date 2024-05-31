import geojson
from pykml import parser
from shapely.geometry import Point
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module='pykml')

# Function to parse KML file and extract police station data
def parse_kml(file_path):
    with open(file_path, 'rt', encoding='utf-8') as f:
        doc = parser.parse(f).getroot()
    
    police_stations = []
    for placemark in doc.Document.Folder.Placemark:
        name = placemark.name.text
        coordinates = placemark.Point.coordinates.text.strip().split(',')
        longitude = float(coordinates[0])
        latitude = float(coordinates[1])
        police_stations.append({
            'name': name,
            'longitude': longitude,
            'latitude': latitude
        })
    return police_stations

# Parse the KML file
police_stations = parse_kml('/Users/ohungchan/Downloads/SPFEstablishments.kml')

# Print the parsed data (for verification)
for station in police_stations:
    print(f"{station['name']}: ({station['latitude']}, {station['longitude']})")

# Load the GeoJSON file
with open('/Users/ohungchan/Downloads/SingaporePoliceForceNPCBoundary.geojson', 'r') as f:
    geojson_data = geojson.load(f)

# Convert police stations to GeoJSON features
police_station_features = []
for station in police_stations:
    point = geojson.Point((station['longitude'], station['latitude']))
    feature = geojson.Feature(geometry=point, properties={"name": station['name']})
    police_station_features.append(feature)

# Add the police station features to the GeoJSON data
if 'features' not in geojson_data:
    geojson_data['features'] = []

geojson_data['features'].extend(police_station_features)

# Save the updated GeoJSON file
output_file_path = '/Users/ohungchan/Downloads/singapore_with_police_stations.geojson'
with open(output_file_path, 'w') as f:
    geojson.dump(geojson_data, f)

print(f"Police stations added and GeoJSON file saved as '{output_file_path}'")

import pandas as pd
import folium
from xml.etree import ElementTree as ET

# Load the KML file
kml_file_path = 'data/case 22 customer (1).kml'
tree = ET.parse(kml_file_path)
root = tree.getroot()

# Define namespaces
namespaces = {
    'kml': 'http://www.opengis.net/kml/2.2',
    'gx': 'http://www.google.com/kml/ext/2.2',
    'atom': 'http://www.w3.org/2005/Atom'
}

# Extract data
data = []
for placemark in root.findall('.//kml:Placemark', namespaces):
    name = placemark.find('kml:name', namespaces).text
    coordinates = placemark.find('.//kml:coordinates', namespaces).text
    data.append([name, coordinates.strip()])

# Create DataFrame
df = pd.DataFrame(data, columns=['Store Name', 'Coordinates'])

# Function to parse coordinates from the KML format
def parse_coordinates(coord_string):
    lon, lat, _ = map(float, coord_string.split(','))
    return lat, lon

# Create a base map
map_center = [10.762622, 106.660172]  # Center the map around Ho Chi Minh City for this example
mymap = folium.Map(location=map_center, zoom_start=12)

# Add markers to the map
for idx, row in df.iterrows():
    lat, lon = parse_coordinates(row['Coordinates'])
    folium.Marker([lat, lon], popup=row['Store Name']).add_to(mymap)

# Save the map to an HTML file
map_file_path = 'data/map_case_22customer.html'
mymap.save(map_file_path)

print(f"Map saved to {map_file_path}")

import folium
import requests
import polyline
import pandas as pd

# Your GraphHopper API Key
API_KEY = "555ea4ea-895a-4505-bc28-43c828c7a909"   # Replace this with your actual GraphHopper API key

# Load coordinates from Excel file
file_path = "./data/Locations_cluster_TONGHOP.xlsx"
df = pd.read_excel(file_path)

# Extract locations from dataframe
locations = [(row["Vĩ độ"], row["Kinh độ"], f"Place {row['No']}") for _, row in df.iterrows()]
locations[0] = (df.iloc[0]["Vĩ độ"], df.iloc[0]["Kinh độ"], "DEPOT")  # Ensure the first point is labeled as DEPOT


# List of routes
routes = [
    [0, 28, 23, 24, 25, 14, 13, 12, 0],
    [0, 26, 27, 22, 34, 0],
    [0, 21, 20, 15, 19, 36, 10, 0],
    [0, 17, 35, 33, 16, 31, 32, 18, 0],
    [0, 30, 9, 5, 29, 3, 4, 0],
    [0, 7, 6, 1, 2, 8, 11, 0],

    [0, 90, 92, 87, 69, 40, 0],
    [0, 72, 70, 78, 45, 56, 0],
    [0, 71, 84, 91, 66, 0],
    [0, 81, 55, 94, 86, 68, 0],
    [0, 98, 80, 64, 58, 60, 48, 0],
    [0, 73, 53, 61, 63, 93, 41, 0],
    [0, 38, 76, 43, 42, 0],
    [0, 82, 59, 67, 62, 50, 75, 0],
    [0, 74, 51, 49, 46, 83, 0],
    [0, 96, 95, 47, 88, 54, 57, 52, 0],
    [0, 99, 89, 97, 85, 39, 0],
    [0, 44, 79, 37, 77, 65, 0],

    [0, 106, 107, 109, 108, 116, 115, 113, 0],
    [0, 119, 112, 117, 114, 0],
    [0, 120, 121, 123, 124, 131, 0],
    [0, 122, 111, 100, 101, 132, 0],
    [0, 110, 103, 118, 127, 126, 125, 0],
    [0, 130, 104, 105, 129, 102, 128, 0],

    [0, 163, 142, 162, 140, 152, 0],
    [0, 139, 164, 141, 151, 138, 166, 0],
    [0, 144, 155, 145, 143, 0],
    [0, 165, 137, 136, 135, 168, 146, 147, 0],
    [0, 154, 157, 153, 134, 133, 0],
    [0, 160, 158, 161, 167, 0],
    [0, 159, 156, 150, 149, 148, 0],

    [0, 172, 175, 170, 177, 169, 0],
    [0, 187, 183, 178, 171, 199, 0],
    [0, 192, 181, 176, 180, 173, 174, 190, 0],
    [0, 197, 194, 182, 186, 198, 191, 200, 0],
    [0, 184, 188, 185, 189, 193, 195, 0],
    [0, 196, 179, 0]
]

# Colors for routes
# colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'cadetblue', 'beige', 'darkblue', 'darkgreen']

colors = [
    'red', 'green', 'blue', 'purple', 'orange', 'darkblue', 'cyan',
    'magenta', 'yellow', 'brown', 'pink', 'grey', 'lime', 'black',
    'teal', 'navy', 'olive', 'gold', 'darkred', 'darkgreen',
    'coral', 'indigo', 'maroon', 'turquoise', 'violet', 'darkslategray',
    'chartreuse', 'crimson', 'orchid', 'firebrick', 'plum', 'salmon',
    'darkkhaki', 'mediumblue', 'steelblue', 'lavender', 'darkorange'
]

# Create a map centered around the DEPOT with a dark theme
map = folium.Map(location=[10.6529637, 106.734935], zoom_start=12, tiles='CartoDB dark_matter')

# Add markers for each location
for i, loc in enumerate(locations):
    if i == 0:
        folium.Marker(
            location=[loc[0], loc[1]],
            icon=folium.DivIcon(
                html='''
                    <div style="
                        background-color: blue;
                        color: white;
                        font-size: 12px;
                        font-weight: bold;
                        text-align: center;
                        border-radius: 50%;
                        width: 30px;
                        height: 30px;
                        display: flex;
                        justify-content: center;
                        align-items: center;">
                        Depot
                    </div>
                '''
            )
        ).add_to(map)
    else:
        folium.Marker(
            location=[loc[0], loc[1]],
            icon=folium.DivIcon(
                html=f'''
                    <div style="
                        background-color: red;
                        color: white;
                        font-size: 12px;
                        font-weight: bold;
                        text-align: center;
                        border-radius: 50%;
                        width: 20px;
                        height: 20px;
                        display: flex;
                        justify-content: center;
                        align-items: center;">
                        {i}
                    </div>
                '''
            )
        ).add_to(map)

# Fetch and draw each route
for idx, route in enumerate(routes):
    route_coords = []
    for i in range(len(route) - 1):
        coord1 = locations[route[i]]
        coord2 = locations[route[i + 1]]

        # Construct the request URL
        url = f'https://graphhopper.com/api/1/route?vehicle=car&locale=en&calc_points=true&key={API_KEY}&point={coord1[0]},{coord1[1]}&point={coord2[0]},{coord2[1]}'
        response = requests.get(url)
        data = response.json()

        # Extract and decode the polyline
        points = data['paths'][0]['points']
        decoded_points = polyline.decode(points, geojson=False)

        # Collect route coordinates
        route_coords.extend(decoded_points)

    # Draw the route on the map
    folium.PolyLine(
        route_coords,
        color=colors[idx % len(colors)],
        weight=5,
        opacity=0.5,
        popup=f'Route {idx + 1}'
    ).add_to(map)

# Add a legend for route colors (only for the number of routes available)
legend_html = '''
<div style="position: fixed; 
            bottom: 50px; left: 50px; width: 200px; height: auto; 
            background-color: white; z-index:9999; font-size:14px; 
            border:2px solid grey; padding: 10px;">
    <h4 style="margin-top: 0;">Route Colors</h4>
    <ul style="list-style-type: none; padding-left: 0;">
'''

# Chỉ hiển thị đúng số lượng routes hiện có
for idx in range(len(routes)):  # ✅ Chỉ lặp qua số route có trong danh sách routes
    legend_html += f'<li><span style="display:inline-block; width:20px; height:20px; background-color:{colors[idx]}; margin-right:10px;"></span>Route {idx + 1}</li>'

legend_html += '</ul></div>'

map.get_root().html.add_child(folium.Element(legend_html))


# Save the map
map.save('./data out/ map_with_legend_Case200.html')
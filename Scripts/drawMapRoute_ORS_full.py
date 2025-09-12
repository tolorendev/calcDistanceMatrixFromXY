import os
import time
import openrouteservice
import folium
import pandas as pd
from openrouteservice import exceptions

# ====== CONFIG ======
API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImE1MjNmNjIyNzlhZDQ5NWU4Nzk3MzgzODBhM2Q1Mjg2IiwiaCI6Im11cm11cjY0In0="  # ⚠️ thay bằng key thật
OUTPUT_HTML = "./data_out/map_with_legend_ORS_full.html"
SLEEP_BETWEEN_ROUTES = 1  # giãn cách giữa các call để tránh 429
RADIUS_LOOSE = 2000          # nới bán kính snap vào mạng đường khi gặp 2010
# =====================

client = openrouteservice.Client(key=API_KEY)

# Load coordinates from Excel file
file_path = "./data/Locations_cluster_TONGHOP.xlsx"
df = pd.read_excel(file_path)

# Extract locations (ORS yêu cầu [lon, lat])
locations = [(row["Kinh độ"], row["Vĩ độ"], f"Place {row['No']}") for _, row in df.iterrows()]
locations[0] = (df.iloc[0]["Kinh độ"], df.iloc[0]["Vĩ độ"], "DEPOT")  # depot

# Danh sách routes
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

colors = [
    'red', 'green', 'blue', 'purple', 'orange', 'darkblue', 'cyan',
    'magenta', 'yellow', 'brown', 'pink', 'grey', 'lime', 'black',
    'teal', 'navy', 'olive', 'gold', 'darkred', 'darkgreen',
    'coral', 'indigo', 'maroon', 'turquoise', 'violet', 'darkslategray',
    'chartreuse', 'crimson', 'orchid', 'firebrick', 'plum', 'salmon',
    'darkkhaki', 'mediumblue', 'steelblue', 'lavender', 'darkorange'
]

# Tạo map nền tối
m = folium.Map(location=[10.6529637, 106.734935], zoom_start=12, tiles='CartoDB dark_matter')

# Add markers
for i, loc in enumerate(locations):
    if i == 0:
        folium.Marker(
            location=[loc[1], loc[0]],
            icon=folium.DivIcon(html='''
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
            ''')
        ).add_to(m)
    else:
        folium.Marker(
            location=[loc[1], loc[0]],
            icon=folium.DivIcon(html=f'''
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
            ''')
        ).add_to(m)

def idx_to_lonlat(idx):
    lon, lat, _ = locations[idx]
    return [float(lon), float(lat)]

def call_directions_multi(coords, use_radiuses=False):
    """Gọi ORS cho 1 route đa điểm. Trả về list [lon,lat] của polyline hoặc None nếu fail."""
    kwargs = dict(
        coordinates=coords,
        profile="driving-car",
        format="geojson",
        instructions=False
    )
    if use_radiuses:
        # nới bán kính cho từng waypoint
        kwargs["radiuses"] = [RADIUS_LOOSE] * len(coords)
    return client.directions(**kwargs)

def call_directions_pair(a, b, use_radiuses=False):
    """Fallback gọi theo cặp, trả về feature geojson hoặc None."""
    kwargs = dict(
        coordinates=[a, b],
        profile="driving-car",
        format="geojson",
        instructions=False
    )
    if use_radiuses:
        kwargs["radiuses"] = [RADIUS_LOOSE, RADIUS_LOOSE]
    return client.directions(**kwargs)

def polyline_to_latlon(geojson_feature):
    coords = geojson_feature["features"][0]["geometry"]["coordinates"]
    return [(lat, lon) for lon, lat in coords]  # folium cần [lat,lon]

# Vẽ các tuyến đường
os.makedirs(os.path.dirname(OUTPUT_HTML), exist_ok=True)

for ridx, route in enumerate(routes):
    # 1) cố gắng gọi 1 lần cho cả route
    coord_list = [idx_to_lonlat(idx) for idx in route]
    try:
        res = call_directions_multi(coord_list, use_radiuses=False)
    except exceptions.ApiError as e:
        # nếu là 2010 (không snap được) → thử lại với radiuses nới
        if "2010" in str(e) or "Could not find routable point" in str(e):
            try:
                res = call_directions_multi(coord_list, use_radiuses=True)
            except Exception:
                res = None
        else:
            # nếu là 429/khác → chờ rồi thử lại một lần
            time.sleep(1.2)
            try:
                res = call_directions_multi(coord_list, use_radiuses=False)
            except Exception:
                res = None
    except Exception:
        res = None

    route_coords_latlon = []

    if res:
        route_coords_latlon = polyline_to_latlon(res)
    else:
        # 2) FALLBACK: chia nhỏ theo từng cặp, cố gắng vẽ được phần nào hay phần đó
        print(f"⚠️ Route {ridx+1}: fallback theo cặp waypoint (có thể do 2010).")
        for i in range(len(route)-1):
            a = idx_to_lonlat(route[i])
            b = idx_to_lonlat(route[i+1])
            seg = None
            try:
                seg = call_directions_pair(a, b, use_radiuses=False)
            except exceptions.ApiError as e:
                if "2010" in str(e) or "Could not find routable point" in str(e):
                    # nới bán kính cho cặp này
                    try:
                        seg = call_directions_pair(a, b, use_radiuses=True)
                    except Exception:
                        seg = None
                else:
                    # có thể là 429 → nghỉ tí rồi thử lại 1 lần
                    time.sleep(1.2)
                    try:
                        seg = call_directions_pair(a, b, use_radiuses=False)
                    except Exception:
                        seg = None

            if seg:
                route_coords_latlon.extend(polyline_to_latlon(seg))
            else:
                print(f"   ⚠️ Bỏ qua đoạn {route[i]} → {route[i+1]} (không routable).")

    if route_coords_latlon:
        folium.PolyLine(
            route_coords_latlon,
            color=colors[ridx % len(colors)],
            weight=5,
            opacity=0.5,
            popup=f'Route {ridx + 1}'
        ).add_to(m)

    # Chống 429: nghỉ giữa các tuyến
    time.sleep(SLEEP_BETWEEN_ROUTES)

# Thêm legend
legend_html = '''
<div style="position: fixed; 
            bottom: 50px; left: 50px; width: 220px; height: auto; 
            background-color: white; z-index:9999; font-size:14px; 
            border:2px solid grey; padding: 10px;">
    <h4 style="margin-top: 0;">Route Colors</h4>
    <ul style="list-style-type: none; padding-left: 0; max-height: 300px; overflow:auto;">
'''
for idx in range(len(routes)):
    legend_html += f'<li><span style="display:inline-block; width:20px; height:20px; background-color:{colors[idx % len(colors)]}; margin-right:10px;"></span>Route {idx + 1}</li>'
legend_html += '</ul></div>'

m.get_root().html.add_child(folium.Element(legend_html))

m.save(OUTPUT_HTML)
print(f"✅ Đã lưu bản đồ với ORS: {OUTPUT_HTML}")

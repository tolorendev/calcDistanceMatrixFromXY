import requests
import folium

# API key của bạn từ GraphHopper
api_key = 'b782da33-bc93-4ec8-9b71-d4b6a00853aa'

def get_distance_graphhopper(lat1, lon1, lat2, lon2, api_key):
    # URL của GraphHopper API
    url = f"https://graphhopper.com/api/1/route?point={lat1},{lon1}&point={lat2},{lon2}&vehicle=car&locale=en&key={api_key}&calc_points=false"

    # Gửi yêu cầu GET tới API
    response = requests.get(url)
    data = response.json()

    # Kiểm tra nếu khóa 'paths' tồn tại trong dữ liệu trả về
    if 'paths' in data:
        # Lấy khoảng cách từ kết quả trả về
        distance = data['paths'][0]['distance'] / 1000  # Chuyển đổi từ mét sang kilomet
        return distance
    else:
        print("Lỗi: Không thể lấy dữ liệu khoảng cách từ API")
        return None

# Tọa độ của hai điểm
lat1 = 10.6072384967056  # Vĩ độ của điểm 1
lon1 = 107.024278842327  # Kinh độ của điểm 1

lat2 =10.8321343 # Vĩ độ của điểm 2
lon2 =107.365823 # Kinh độ của điểm 2

# Tính toán khoảng cách
distance = get_distance_graphhopper(lat1, lon1, lat2, lon2, api_key)

# In kết quả ra console
if distance is not None:
    print(f"Khoảng cách giữa hai điểm là: {distance:.2f} km")

# Vẽ bản đồ với hai điểm
map_center = [(lat1 + lat2) / 2, (lon1 + lon2) / 2]
mymap = folium.Map(location=map_center, zoom_start=12)

# Thêm hai điểm lên bản đồ
folium.Marker([lat1, lon1], popup="Điểm 1", tooltip="Điểm 1").add_to(mymap)
folium.Marker([lat2, lon2], popup="Điểm 2", tooltip="Điểm 2").add_to(mymap)

# Vẽ đường nối hai điểm
folium.PolyLine(locations=[[lat1, lon1], [lat2, lon2]], color="blue", weight=2.5, opacity=1).add_to(mymap)

# Lưu bản đồ vào file HTML và hiển thị
mymap.save("./data/map_with_two_points.html")
print("Bản đồ đã được lưu vào file map_with_two_points.html")

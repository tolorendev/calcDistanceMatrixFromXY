import requests
import json

# Thay 'your_api_key_here' bằng khóa API của bạn từ GraphHopper
API_KEY = '658985e7-8063-48ad-9a77-1c96bd0e2c9c'

# Danh sách các địa điểm (tọa độ)
locations = [
    (40.712776, -74.005974), # New York, NY
    (34.052235, -118.243683), # Los Angeles, CA
    (41.878113, -87.629799), # Chicago, IL
    (29.760427, -95.369804), # Houston, TX
    (33.448376, -112.074036) # Phoenix, AZ
]

# URL cơ bản cho yêu cầu API
base_url = f'https://graphhopper.com/api/1/route?vehicle=car&locale=en&calc_points=true&key={API_KEY}'

# Hàm tạo chuỗi các điểm cho yêu cầu API
def create_url_with_points(base_url, locations):
    for lat, lon in locations:
        base_url += f'&point={lat},{lon}'
    return base_url

# Tạo URL hoàn chỉnh với các điểm
url = create_url_with_points(base_url, locations)

# Gửi yêu cầu đến API
response = requests.get(url)
data = response.json()

# Kiểm tra kết quả trả về
if 'paths' in data:
    for path in data['paths']:
        distance = path['distance'] / 1000  # chuyển đổi sang km
        time = path['time'] / 1000 / 60  # chuyển đổi sang phút
        print(f"Khoảng cách: {distance} km, Thời gian: {time} phút")
else:
    print("Có lỗi xảy ra:", data)

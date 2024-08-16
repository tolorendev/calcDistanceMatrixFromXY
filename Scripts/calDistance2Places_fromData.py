import pandas as pd
import requests

# API key từ GraphHopper
api_key = '69b3a042-0bda-4fca-bd6e-34874e9577e9'  # mail nambk

# Đọc dữ liệu từ file Excel
file_path = './data/Locations_Data_4.xlsx'
sheet_name = 'ver1'

df = pd.read_excel(file_path, sheet_name=sheet_name)

# Hàm để tính khoảng cách giữa hai điểm bằng GraphHopper
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

# Hàm để lấy tọa độ từ chỉ số
def get_coordinates(index, dataframe):
    return dataframe.loc[index, 'Vĩ độ'], dataframe.loc[index, 'Kinh độ']

# Nhập vào chỉ số của hai điểm
point1 = int(input("Nhập chỉ số của điểm 1 (0-200): "))
point2 = int(input("Nhập chỉ số của điểm 2 (0-200): "))

# Lấy tọa độ của hai điểm
lat1, lon1 = get_coordinates(point1, df)
lat2, lon2 = get_coordinates(point2, df)

# Tính toán khoảng cách
distance = get_distance_graphhopper(lat1, lon1, lat2, lon2, api_key)

# In kết quả ra console
if distance is not None:
    print(f"Khoảng cách giữa điểm {point1} và điểm {point2} là: {distance:.2f} km")

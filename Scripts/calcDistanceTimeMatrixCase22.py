import requests
import json
import pandas as pd

# Thay 'your_api_key_here' bằng khóa API của bạn từ GraphHopper
API_KEY = 'f4d4989b-47fd-4664-84bb-08a51b2df36c'
VEHICLE_TYPE = 'truck'  # Thay đổi loại phương tiện tại đây (car, bike, foot, truck)


# Danh sách các địa điểm (tọa độ)
# locations = [
# (10.634246676314339, 106.76417883127394),  # DEPOT
# (10.6514735, 106.7296985),  # Place 1
# (10.6323308, 106.7359172),  # Place 2
# (10.7129109, 106.6987578),  # Place 3
# (10.7184916, 106.6995137),  # Place 4
# (10.7094096, 106.7023472),  # Place 5
# (10.6879035, 106.7420862),  # Place 6
# (10.6663564, 106.7251708),  # Place 7
# (10.6524738, 106.7296984),  # Place 8
# (10.69348, 106.7407434),  # Place 9
# (10.6661552, 106.6953776),  # Place 10
# (10.6970672, 106.7186401),  # Place 11
# (10.6367573, 106.7347741),  # Place 12
# (10.7361417, 106.7301419),  # Place 13
# (10.7392916, 106.7302549),  # Place 14
# (10.7389107, 106.7034739),  # Place 15
# (10.7550576, 106.7210508),  # Place 16
# (10.7516601, 106.7028717),  # Place 17
# (10.7404025, 106.6969),  # Place 18
# (10.7467691, 106.710208),  # Place 19
# (10.7317828, 106.735252),  # Place 20
# (10.7277268, 106.7329311),  # Place 21
# (10.7456183, 106.715932),  # Place 22
#
# ]

locations = [
    (10.631424, 106.763047), # Vicem hạ long
    (10.666356, 106.725171), # Cửa hàng vật liệu xây dựng Tấn Phát 1
    (10.652474, 106.729698), # Cửa Hàng Vật Liệu Xây Dựng Phú Cường
    (10.666641, 106.724994), # Cửa hàng vật liệu xây dựng
    (10.705958, 106.703453), # Nguyen Tri Linh Trung Building Material Store
    (10.657063, 106.715584), # cửa hàng vật liệu xây dựng lê chính
    (10.679833, 106.701396), # Vlxd phước thịnh phát
    (10.687904, 106.742086), # Cửa Hàng VLXD Thuận Phát 484/4
    (10.706705, 106.703144), # Cửa hàng vật liệu xây dựng & trang trí nội thất An Phát
    (10.882154, 106.628766), # Vật Liệu Xây Dựng- Trang Trí Nội Thất Quốc Hải
    (10.814462, 106.775176), # Vật liệu xây dựng Vân Anh
    (10.666155, 106.695378), # Cửa hàng vlxd WeHome nhà Bè
    (10.69348, 106.740743),  # Cửa Hàng VLXD - TTNT Nam Phát
    (10.709409, 106.702346), # Cửa hàng VLXD & TTNT NAM PHÁT THỊNH
    (10.712911, 106.698758), # Cửa Hàng Vlxd Khánh Ân
    (10.69556, 106.739736),  # Cửa Hàng VLXD Tài Lộc 1
    (10.636102, 106.719487), # Công ty cổ phần Long Hậu
    (10.63245, 106.726844),  # Nhà xưởng cao tầng Long Hậu
    (10.7141956, 106.7376459), # VẬT LIỆU XÂY DỰNG TRƯỜNG THỊNH PHÁT
    (10.7456182, 106.7159358), # Vật liệu xây dựng Cần Kiệm Phát
    (10.8029288, 106.7084131), # Vật Liệu Xây Dựng Trung Hiếu
]

# Tạo danh sách các cặp địa điểm
pairs = [(i, j) for i in range(len(locations)) for j in range(i+1, len(locations))]

# Hàm gửi yêu cầu API và lấy khoảng cách, thời gian
def get_distance_time(coord1, coord2):
    url = f'https://graphhopper.com/api/1/route?vehicle={VEHICLE_TYPE}&locale=en&calc_points=true&key={API_KEY}&point={coord1[0]},{coord1[1]}&point={coord2[0]},{coord2[1]}'
    response = requests.get(url)
    data = response.json()
    if 'paths' in data:
        distance = data['paths'][0]['distance'] / 1000  # chuyển đổi sang km
        time = data['paths'][0]['time'] / 1000 / 60  # chuyển đổi sang phút
        return distance, time
    else:
        return None, None

# Tạo ma trận khoảng cách và thời gian
distance_matrix = [[0]*len(locations) for _ in range(len(locations))]
time_matrix = [[0]*len(locations) for _ in range(len(locations))]

# Điền dữ liệu vào ma trận
for i, j in pairs:
    distance, time = get_distance_time(locations[i], locations[j])
    distance_matrix[i][j] = distance_matrix[j][i] = distance
    time_matrix[i][j] = time_matrix[j][i] = time

# Chuyển ma trận thành DataFrame và lưu vào Excel
distance_df = pd.DataFrame(distance_matrix, columns=[f'Place {i}' for i in range(len(locations))], index=[f'Place {i}' for i in range(len(locations))])
time_df = pd.DataFrame(time_matrix, columns=[f'Place {i}' for i in range(len(locations))], index=[f'Place {i}' for i in range(len(locations))])

with pd.ExcelWriter('distance_time_matrix_case22.xlsx') as writer:
    distance_df.to_excel(writer, sheet_name='Distance Matrix')
    time_df.to_excel(writer, sheet_name='Time Matrix')


import requests
import numpy as np
import pandas as pd

# API key từ GraphHopper
api_key = '1c9c4f2c-49d5-4952-a9c7-c35e6a9f4793'

# Đọc tọa độ từ file Excel
input_file = './data/input_location_data.xlsx'  # Đường dẫn đến file Excel
df = pd.read_excel(input_file)

# Chuyển dữ liệu thành list các tọa độ
locations = df[['Vĩ độ', 'Kinh độ']].values.tolist()

# Số lượng địa điểm
num_locations = len(locations)

# Tạo ma trận khoảng cách
distance_matrix = np.zeros((num_locations, num_locations))

# Tổng số vòng lặp
total_iterations = num_locations * (num_locations - 1)

# Biến đếm để theo dõi số lần lặp
iteration_count = 0

# Lặp qua tất cả các cặp địa điểm
for i in range(num_locations):
    for j in range(num_locations):
        if i != j:
            iteration_count += 1
            print(f"Đang xử lý lần lặp thứ {iteration_count}/{total_iterations} (từ điểm {i + 1} đến điểm {j + 1})...")

            url = f"https://graphhopper.com/api/1/route?point={locations[i][0]},{locations[i][1]}&point={locations[j][0]},{locations[j][1]}&vehicle=car&locale=en&key={api_key}&calc_points=false"
            response = requests.get(url)
            data = response.json()

            # Kiểm tra nếu khóa 'paths' tồn tại trong dữ liệu trả về
            if 'paths' in data:
                # Lấy khoảng cách từ kết quả trả về
                distance = data['paths'][0]['distance'] / 1000  # Chuyển đổi từ mét sang kilomet
                distance_matrix[i][j] = distance
                print(f"Khoảng cách từ điểm {i + 1} đến điểm {j + 1}: {distance:.2f} km")
            else:
                # Ghi lại thông báo lỗi nếu không có đường dẫn hợp lệ
                print(f"Lỗi: Không tìm thấy 'paths' cho cặp tọa độ ({locations[i]}, {locations[j]})")
                distance_matrix[i][j] = np.nan  # Có thể gán giá trị NaN hoặc một giá trị đặc biệt để đánh dấu lỗi
        else:
            distance_matrix[i][j] = 0  # Khoảng cách đến chính nó bằng 0
            print(f"Khoảng cách từ điểm {i + 1} đến chính nó: 0 km")

# Xuất ma trận khoảng cách ra file Excel
output_file = './data/distance_matrix_output.xlsx'  # Đường dẫn đến file Excel xuất ra
df_output = pd.DataFrame(distance_matrix)
df_output.to_excel(output_file, index=False, header=False)

print(f"Ma trận khoảng cách đã được ghi vào file {output_file}")

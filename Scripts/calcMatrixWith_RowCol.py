import pandas as pd
import numpy as np
import requests

# API key từ GraphHopper
api_key = '1c9c4f2c-49d5-4952-a9c7-c35e6a9f4793'

# Đọc tọa độ từ các file Excel
input_file_col = './data/input_location_col.xlsx'
input_file_row = './data/input_location_row.xlsx'

df_col = pd.read_excel(input_file_col)
df_row = pd.read_excel(input_file_row)

# Chuyển dữ liệu thành danh sách các tọa độ
locations_col = df_col[['Vĩ độ', 'Kinh độ']].values.tolist()
locations_row = df_row[['Vĩ độ', 'Kinh độ']].values.tolist()

# Số lượng địa điểm
num_col_locations = len(locations_col)
num_row_locations = len(locations_row)

# Tạo ma trận khoảng cách
distance_matrix = np.zeros((num_row_locations, num_col_locations))

# Tổng số vòng lặp
total_iterations = num_row_locations * num_col_locations

# Biến đếm để theo dõi số lần lặp
iteration_count = 0

# Lặp qua tất cả các cặp địa điểm
for i in range(num_row_locations):
    for j in range(num_col_locations):
        iteration_count += 1
        print(
            f"Đang xử lý lần lặp thứ {iteration_count}/{total_iterations} (từ điểm hàng {i + 1} đến điểm cột {j + 1})...")

        url = f"https://graphhopper.com/api/1/route?point={locations_row[i][0]},{locations_row[i][1]}&point={locations_col[j][0]},{locations_col[j][1]}&vehicle=car&locale=en&key={api_key}&calc_points=false"
        response = requests.get(url)
        data = response.json()

        # Kiểm tra nếu khóa 'paths' tồn tại trong dữ liệu trả về
        if 'paths' in data:
            # Lấy khoảng cách từ kết quả trả về
            distance = data['paths'][0]['distance'] / 1000  # Chuyển đổi từ mét sang kilomet
            distance_matrix[i][j] = distance
            print(f"Khoảng cách từ điểm hàng {i + 1} đến điểm cột {j + 1}: {distance:.2f} km")
        else:
            # Ghi lại thông báo lỗi nếu không có đường dẫn hợp lệ
            print(f"Lỗi: Không tìm thấy 'paths' cho cặp tọa độ ({locations_row[i]}, {locations_col[j]})")
            distance_matrix[i][j] = np.nan  # Đánh dấu lỗi với giá trị NaN

# Xuất ma trận khoảng cách ra file Excel
output_file = './data/distance_matrix_output_rowCol.xlsx'
df_output = pd.DataFrame(distance_matrix)
df_output.to_excel(output_file, index=False, header=False)

print(f"Ma trận khoảng cách đã được ghi vào file {output_file}")

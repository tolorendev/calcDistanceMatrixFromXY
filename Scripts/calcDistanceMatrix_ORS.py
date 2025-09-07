import openrouteservice
import pandas as pd
import numpy as np

# 🔑 API key từ OpenRouteService
api_key = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImE1MjNmNjIyNzlhZDQ5NWU4Nzk3MzgzODBhM2Q1Mjg2IiwiaCI6Im11cm11cjY0In0=" #mail giabao1005
client = openrouteservice.Client(key=api_key)

# 📂 Đọc file Excel chứa tọa độ (cột: Kinh độ, Vĩ độ)
input_file = "data/input_location_data.xlsx"
df = pd.read_excel(input_file)

# ⚠️ ORS yêu cầu tọa độ dạng [lon, lat] (Kinh độ trước, Vĩ độ sau)
locations = df[['Kinh độ', 'Vĩ độ']].values.tolist()

# 🚗 Gọi Matrix API (chỉ 1 lần)
matrix = client.distance_matrix(
    locations=locations,
    profile='driving-car',   # có thể đổi thành 'driving-hgv', 'cycling-regular', 'foot-walking'
    metrics=['distance'],    # có thể thêm 'duration' nếu cần
    units='km'
)

# 📊 Lấy kết quả ma trận khoảng cách
distance_matrix = np.array(matrix['distances'])

# 💾 Xuất ra Excel
output_file = "data/distance_matrix_output_ors.xlsx"
df_output = pd.DataFrame(distance_matrix)
df_output.to_excel(output_file, index=False, header=False)

print(f"✅ Ma trận khoảng cách đã được ghi vào file {output_file}")

import openrouteservice
import folium

# API key
client = openrouteservice.Client(key="eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImE1MjNmNjIyNzlhZDQ5NWU4Nzk3MzgzODBhM2Q1Mjg2IiwiaCI6Im11cm11cjY0In0=")

# Điểm [lon, lat]
start = [106.7009, 10.7769]  # Hồ Con Rùa, TP.HCM
end   = [106.6602, 10.7626]  # Sân bay Tân Sơn Nhất

# Gọi Directions API
route = client.directions(
    coordinates=[start, end],
    profile='driving-car',
    format='geojson'
)

# Tạo map
m = folium.Map(location=[10.77, 106.69], zoom_start=13)
folium.GeoJson(route, name="route").add_to(m)
folium.Marker(location=start[::-1], tooltip="Start").add_to(m)
folium.Marker(location=end[::-1], tooltip="End").add_to(m)

m.save("route_map.html")
print("✅ Đã lưu bản đồ route trong file route_map.html")

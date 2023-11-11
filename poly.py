import requests
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt

apiToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcHBJZCI6InF0ZXQ0cjNva2UiLCJ0b2tlbiI6eyJpdiI6ImFkMDQxYzVlYTY5YzI2OTgyMGQ2MjYzYmU5NGEzODBlIiwiY29udGVudCI6IjUzNDFlZmQ3NTJmNDNjMjk2OGQ0YWNjMGVmYWQ0MTgwNmYwZmM3N2E2NjgyZjQ2YTEzNGU0YmUyNmQzYWM4ZTMwN2VlY2Q5NTQ1MGExMGQ2MjYzMDI0N2NlNzYxYzhiZmRmYmQ4MWMzMmY0NzA5ZGYyYjJkMmNjOTRiMTAyOWQ0Yjc1YTRjMWYzODgxZmNjYTgzMmUyYjA0ZWNkMmJlY2NjNDgzYzliNmFiNWNjOTc2OTQwYWVjM2M4MTAwZGZlNDFlN2E0YTYxYjNmMjNhZjM0ZmM2YjJhOGMwY2M2MmVlMDk0NDExYmY3ZjI5NjQwMWIzZWVjYzA4NTI4ZWQyZDQ4M2RmZGI1MDg4YmEwY2E3YjJlNDExMjkzMTZjMGE1ZmI0Y2ZhMjQyNmRiMzM0NTUxZmY4NzYwYzVkNWM2YzA3OGFiMjIyNWRlNWIyZWFkNDc5ZTViZDdlOGE0YTI1ODJiZjVmYTY0YzJhNTlhOGIyYjZmMzRhNzdjYzIxYmVmODAyYTM4YzZlNDNhODhiYmNjMTg5OGQ0ODY5MGI5MjkzMjYyZDA1YTQ2OTA1NjgxOTlhNzViMmJkZWEyODgzZmZjMWZkMDAxMDY4ZTQ3MzUxNzU2NTU1YTRmNTAzZTU3ZjI0NWQ1NjdkZWM4OWI5ODI0N2I0NTg3YTc2NDc2N2QyYzA4NWRiYzVjMDgyZGYxNTc2MmY3OTMyYzNkOTg2YTZkNTRjZDI2YmRjYTUxNzQ1ODFlZTJjMzJjMWExYTM0ODFhYWE4MDE5ZmI3ZjY1N2ZkNmEyM2VkMDkzMzUzZTYyNmE0MzdkMjE4ZDljNzEyZTgzYTNmZDNkMDk1NjEyMzdkMWIzZGNiODQ1MjI3MDk3Mjg1N2UxIn0sInNlY3VyaXR5VG9rZW4iOnsiaXYiOiJhZDA0MWM1ZWE2OWMyNjk4MjBkNjI2M2JlOTRhMzgwZSIsImNvbnRlbnQiOiI0MjQ5ZThlNzU2ZDkwYjcxNzBkM2JjYmZkN2IwN2NlMzZkMzBlNTRmNzY5ZGVkM2UwMzY0NDE5YTZjM2E4ZGRmMzNjZmFhZTA1MjI3MmNmMDdhMTIyNTQyIn0sImp0aSI6ImUxYjRlODE3LTYwNTAtNGIwNS1hY2MyLWUxMWNiZTY1YWZmZSIsImlhdCI6MTY5OTc0MjQyNCwiZXhwIjoxNjk5NzQ2MDI0fQ.zU6ZCpCEHd6goFmOJYDxLzEHXj2JBP65_5tPKhGBR2U"

def getPolygon(center_x="37.7749", center_y="-122.4194", rangeType="D", duration=30):
    # url = "https://api.iq.inrix.com/drivetimePolygons?center=37.770315%7C-122.446527&rangeType=A&duration=30"
    url = f"https://api.iq.inrix.com/drivetimePolygons?center={center_x}%7C{center_y}&rangeType={rangeType}&duration={duration}"

    payload = {}
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {apiToken}'
    }

    xml_data = requests.request("GET", url, headers=headers, data=payload)
    # print(xml_data.text)

    # Parse the XML
    root = ET.fromstring(xml_data.text)
    
    polygons = root.findall(".//{http://www.opengis.net/gml}posList")

    polygon = polygons[0].text

    points = [float(coord) for coord in polygon.split()]

    # Reshape the array into pairs of (latitude, longitude)
    points = np.array(points).reshape(-1, 2)

    plt.xlim([-122.55, -122.05])  # Example range for longitude
    plt.ylim([37.4, 38.0])  # Example range for latitude

    # Plot the points
    plt.scatter(points[:, 1], points[:, 0], label='Points')
    plt.title('Scatter Plot of Points')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    

    # Connect the points to form a polygon
    polygon = plt.Polygon(points, edgecolor='r', fill=None, linewidth=2, label='Polygon')
    plt.gca().add_patch(polygon)

    

    # Show the plot
    plt.legend()
    plt.show()

    # Access elements and attributes
    


getPolygon()

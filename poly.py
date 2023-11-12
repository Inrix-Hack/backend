import requests
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt

apiToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcHBJZCI6InF0ZXQ0cjNva2UiLCJ0b2tlbiI6eyJpdiI6IjVmNjhiNzhlNGRhNWZhY2JiYmE2NjUxYWZkNzFhZjgzIiwiY29udGVudCI6ImVjNjE4NjY3YjlhZTdhZTlhNGYyZjg0OWZhZGEwNzQ1Njg5N2YwNjVhYjQxM2I4NWRlYjY5M2Q5ZjAxNjliMGNjNTNjMmE1OWQ1YjU3MDhlNDgzNjY5MGVmOTIwNzg4MWNkYmYzYWVlYTY0YWEyZTI0YzYxYjkxOGYzN2VjNGQ3NWM4NjgwNzMxNzIwNGNjYTkyNDQyNTA1M2YyMjQ0MGJjMmQ4ZWRhZjQ0Y2VhMzM2NmU5NTE2YTkwOTE0NTQzODNmYjM0MTFkODFiMTg4ZjU5NmIyZmQ2OGFkNjc2MzEwNjIxYTljYTQ5ZmVjNTI5NjUxZTg3MjQzNjQ2OWQ1NTNmODJhODQ4Mjc1OWY4ZWYzYzllYmM5NzZlNjVjZTE0MmVmMzg3N2YxMGE4MDVjZGZhNjcwNWI5NTFiMTRlNWYyYjE3NGZhOGUxNWM0ODQzMDIyMjJhM2MyYmMzOGFlZWU3NzUwM2NkMzYzNjdhZGM5ZDE4ZWNjZDI2NjgzZDU2YWE0ZTE3YzkxMGI0YTk2MWFhMTEyYjBkZGUwZWY5M2UzZjEzNTM2YjgwMTQyZGNhMzAwZDdlMjdiY2MzY2QwMDBjNzE4ZDcwZTA4OTMzNjM1Y2UwYjYyYmUyNWMwYjhkOTUxZWU3MjczZjlmNmQ3M2RkMDhlZDgyYjI3MmRmNzlhZjQzYTc0NjVkMGIyMGY5ZDk2OTM1MTE2ODUwNGIyNDc0MzIxNjQyOTJjYzA2MDI3ODgyYzY0ZmVlNjg1ODdhYmM5YTQ1ZDgwMjY3ZTc4OGVjZTdjNzYxZmFkNTc5OTEzYWQ5OTU4NDkwMmFhY2E0OTJjNTE0NmQ4NmRjOTU1N2RkZDYxYjgzMGEwNDM1YTUxMjM1MjA0In0sInNlY3VyaXR5VG9rZW4iOnsiaXYiOiI1ZjY4Yjc4ZTRkYTVmYWNiYmJhNjY1MWFmZDcxYWY4MyIsImNvbnRlbnQiOiJmZDM1OGE0ZGE4YmIyMGQxYWRmM2Y1NzQ5OGQyMjcxMDEyODljZTRjZDA3NjIyZGVlZDgzYWM4M2VhMjdhNTYyYWI0OTBjMjliZWUzMzlmNzdhMTMxNTMwIn0sImp0aSI6IjcwOGQ5YjBiLTU0NmMtNDA0NS04ZjBjLTE5YThhMzVhNTQwNSIsImlhdCI6MTY5OTc0NzgyMCwiZXhwIjoxNjk5NzUxNDIwfQ.5ym6RVGfylzKhhlGTofOMCOkreGSy0qbEEHcOOXKsVI"

<<<<<<< HEAD
def getPolygon(center_x="37.7749", center_y="-122.4194", rangeType="D", duration=30):
    # url = "https://api.iq.inrix.com/drivetimePolygons?center=37.770315%7C-122.446527&rangeType=A&duration=30"
    url = f"https://api.iq.inrix.com/drivetimePolygons?center={center_x}%7C{center_y}&rangeType={rangeType}&duration={duration}"
=======

def getPolygon(center_x="37.7749", center_y="-122.4194"):
    url = f"https://api.iq.inrix.com/drivetimePolygons?center={center_x}%7C{center_y}&rangeType=A&duration=30"
>>>>>>> 2f476e04fa9bccc6f3a32a959d00a1b8417d9567

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

    


print(getPolygon())

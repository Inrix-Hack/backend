import json

apiToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcHBJZCI6InF0ZXQ0cjNva2UiLCJ0b2tlbiI6eyJpdiI6IjVmNjhiNzhlNGRhNWZhY2JiYmE2NjUxYWZkNzFhZjgzIiwiY29udGVudCI6ImVjNjE4NjY3YjlhZTdhZTlhNGYyZjg0OWZhZGEwNzQ1Njg5N2YwNjVhYjQxM2I4NWRlYjY5M2Q5ZjAxNjliMGNjNTNjMmE1OWQ1YjU3MDhlNDgzNjY5MGVmOTIwNzg4MWNkYmYzYWVlYTY0YWEyZTI0YzYxYjkxOGYzN2VjNGQ3NWM4NjgwNzMxNzIwNGNjYTkyNDQyNTA1M2YyMjQ0MGJjMmQ4ZWRhZjQ0Y2VhMzM2NmU5NTE2YTkwOTE0NTQzODNmYjM0MTFkODFiMTg4ZjU5NmIyZmQ2OGFkNjc2MzEwNjIxYTljYTQ5ZmVjNTI5NjUxZTg3MjQzNjQ2OWQ1NTNmODJhODQ4Mjc1OWY4ZWYzYzllYmM5NzZlNjVjZTE0MmVmMzg3N2YxMGE4MDVjZGZhNjcwNWI5NTFiMTRlNWYyYjE3NGZhOGUxNWM0ODQzMDIyMjJhM2MyYmMzOGFlZWU3NzUwM2NkMzYzNjdhZGM5ZDE4ZWNjZDI2NjgzZDU2YWE0ZTE3YzkxMGI0YTk2MWFhMTEyYjBkZGUwZWY5M2UzZjEzNTM2YjgwMTQyZGNhMzAwZDdlMjdiY2MzY2QwMDBjNzE4ZDcwZTA4OTMzNjM1Y2UwYjYyYmUyNWMwYjhkOTUxZWU3MjczZjlmNmQ3M2RkMDhlZDgyYjI3MmRmNzlhZjQzYTc0NjVkMGIyMGY5ZDk2OTM1MTE2ODUwNGIyNDc0MzIxNjQyOTJjYzA2MDI3ODgyYzY0ZmVlNjg1ODdhYmM5YTQ1ZDgwMjY3ZTc4OGVjZTdjNzYxZmFkNTc5OTEzYWQ5OTU4NDkwMmFhY2E0OTJjNTE0NmQ4NmRjOTU1N2RkZDYxYjgzMGEwNDM1YTUxMjM1MjA0In0sInNlY3VyaXR5VG9rZW4iOnsiaXYiOiI1ZjY4Yjc4ZTRkYTVmYWNiYmJhNjY1MWFmZDcxYWY4MyIsImNvbnRlbnQiOiJmZDM1OGE0ZGE4YmIyMGQxYWRmM2Y1NzQ5OGQyMjcxMDEyODljZTRjZDA3NjIyZGVlZDgzYWM4M2VhMjdhNTYyYWI0OTBjMjliZWUzMzlmNzdhMTMxNTMwIn0sImp0aSI6IjcwOGQ5YjBiLTU0NmMtNDA0NS04ZjBjLTE5YThhMzVhNTQwNSIsImlhdCI6MTY5OTc0NzgyMCwiZXhwIjoxNjk5NzUxNDIwfQ.5ym6RVGfylzKhhlGTofOMCOkreGSy0qbEEHcOOXKsVI"

def getFuelStations():
    file = open('fuelStations.json')
    fuelStationRawData = json.load(file)
    fuelStations = []
    for fuelStation in fuelStationRawData['result']:
        x = {
            'name' : fuelStation['name'],
            'coordinates' : fuelStation['geometry']['coordinates'],
        }
        for product in fuelStation['products']:
            if product['type'] == 'Regular':
                x['price'] = product['price']
        if not x.__contains__('price'):
            continue
        fuelStations.append(x)
    return fuelStations


def getRoutes(gases, fuel, mpg, max):
    stations = []
    payload = {}
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {apiToken}'
    }
    for gas in gases:
        name, coordinates, price = gas
        lat, lon = coordinates
        url = ""
        
        response = requests.request("GET", url, headers=headers, data=payload)
        stations.append([response.json()['routes']['id'], gas, ((response.json()['routes']['totalDistance'] / mpg * 2) + (max - fuel)) * price, response.json()['routes']['totalDistance'], response.json()['routes']['travelTimeMinutes']])
    stations.sort(key=lambda x: x[2])

    return [{
        "route" : station[0],
        "station": station[1],
        "distance": station[3]
    } for station in stations[:3]]

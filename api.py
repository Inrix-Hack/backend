import json
from time import sleep

import requests

apiToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcHBJZCI6InF0ZXQ0cjNva2UiLCJ0b2tlbiI6eyJpdiI6IjBmYmYyMDFjYjljYTBiNzRlN2QzZGE3ZmZjMmJiOThhIiwiY29udGVudCI6Ijk1NzEwNmFiNGZlYzRiNmRjODRjNGZkNDkzNzlkYzZhNmU2ZDZiYzY4MjQ0MTBjNjIyOTJhMDIwMTE3OGY0NzA0YTNlNzI0M2VjZmVlNjgzYjBhZWZiMDNhNzVhMmFmNGRmY2E4MjY4NDAyZDFjOGMxZDJmZDBlYWZjNjBjMzZlODNjMTIyNTE1NjZhZGMxYzhlNmY3NjE1ZDY3ZWMxNTk2YjUzNjQ1NWZlNDZmOGRkY2YyODllMWQ2MDAxYzM1MzM4NjM2ZGNkNmVlZGI2OGZjNTEwMjhiMjc0NTQ0ODgxNjBiZGI4OWY1MDVkMDM0YTZkNWZhN2NlNzUyZjhjZWQ5ODJjZmU3MDMzNTdiZjQyZmExMjQxN2I3YjU4NTMxYjgyZTIyZGE3MDBhODAyOTQ0OWIzYWExYzMxN2VhYTJmM2IxNGM4NjQyNjY4YmIyMDlkYTUxMWE5ZWIxNTY3NmJkN2ExNzUyOGRkMjZkNWExM2Q3YjcyYmQ4MmJlNjdiMDI0YWNhY2I5ODZkYzY4YmQ4NzM3N2U5OWZkZjI0NzUzYjA1ZTAyYThhZWVlYTMyMTlkZjEyNjZhODQzMGU0NWI4OTIxY2UwYWRkMTQ5NTE4ZTI5OTA2MTI2NDgzZWI0NDlkYzk0MThkYmJlNjE3YWUzNDVkYWU4NjMyMzZiNzkzYzA2MjJmYTE5OGNiNjQwZGQwNzkxYmE3ZDhiNDJhOWUyYTIzNjhkNmQ5MTlkMzQ4MjA1OWUwNDJiNzc3MWI1NjkxZTA4NDhlNjAyOTAyY2E0NWM2YTljZTcxM2MyYWNlNzE0MDNkOTZhZjEzMmZhNzMxMDE4ZjFmNDEwNjRjOTVlMmZhOWYyMzkzMWM2YjBjMDQ4YzVjIn0sInNlY3VyaXR5VG9rZW4iOnsiaXYiOiIwZmJmMjAxY2I5Y2EwYjc0ZTdkM2RhN2ZmYzJiYjk4YSIsImNvbnRlbnQiOiJhMDRhMDI4NzQ4OTIwMjM0ZTU0MjQ3ZjI4NDc3ZmQxZTYzMjkxN2U3ZmUwMDBkYzAzNmUyOTg3NDBhMjJkMDY0NmIyNDYyMzA4N2FiZDI4Nzk1ZmVkMDNkIn0sImp0aSI6ImMyMzBmOGZhLTVhZTEtNGM2MS04ODFjLTczMjk5ZjQwODI0YyIsImlhdCI6MTY5OTc4NzA5MywiZXhwIjoxNjk5NzkwNjkzfQ.EiwVEzFtl9oPQE7b1jvibS1S2qzld_Ew9r5kinL8YgQ"

startCoordinates = [-122.4799, 37.7241]
endCoordinates = [-122.4125, 37.8086]


def calculateDistance(startCoordinates, endCoordinates):
    return ((startCoordinates[0] - endCoordinates[0]) ** 2 + (startCoordinates[1] - endCoordinates[1]) ** 2) ** 0.5


def calculateRadius(diameter):
    return diameter / 2


def calculateMidPoint(startCoordinates, endCoordinates):
    return [(startCoordinates[0] + endCoordinates[0]) / 2, (startCoordinates[1] + endCoordinates[1]) / 2]


distance = calculateDistance(startCoordinates, endCoordinates)
radius = calculateRadius(distance)
midPoint = calculateMidPoint(startCoordinates, endCoordinates)


def getFuelStations():
    file = open('fuelStations.json')
    fuelStationRawData = json.load(file)
    fuelStations = []
    for fuelStation in fuelStationRawData['result']:
        if calculateDistance(midPoint, fuelStation['geometry']['coordinates']) > radius / 2:
            continue
        x = {
            'name': fuelStation['name'],
            'coordinates': fuelStation['geometry']['coordinates'],
        }
        for product in fuelStation['products']:
            if product['type'] == 'Regular':
                x['price'] = product['price']
        if not x.__contains__('price'):
            continue
        fuelStations.append(x)
    return fuelStations


def getRoutes(gasStations, currentFuelInCar, mpgOfCar, maximumCapacityOfCar):
    payload = {}
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {apiToken}'
    }

    stations = []
    url = "https://api.iq.inrix.com/findRoute?wp_1=37.770581%2C-122.442550&wp_2=37.765297%2C-122.442527&format=json"
    response = requests.request("GET", url, headers=headers, data=payload)
    # print(response.json())
    # return response.json()
    counter = 0
    session = requests.session()
    for gasStation in gasStations[:3]:
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {apiToken}'
        }
        stationName = gasStation['name']
        stationCoordinates = gasStation['coordinates']
        stationPrice = gasStation['price']
        response = session.request("GET", url, headers=headers, data=payload)
        # return response.json()['result']['trip']['routes'][0]
        route = response.json()['result']['trip']['routes'][0]
        # return route
        stations.append([route['id'], gasStation, ((float(route['totalDistance']) / mpgOfCar * 2) + (
                    maximumCapacityOfCar - currentFuelInCar)) * stationPrice, float(route['totalDistance']),
                         float(route['travelTimeMinutes'])])
    stations.sort(key=lambda x: x[2])

    return [{
        "route": station[0],
        "station": station[1],
        "distance": station[3]
    } for station in stations[:3]]

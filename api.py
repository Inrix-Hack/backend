import json
from time import sleep

import requests

apiToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcHBJZCI6InF0ZXQ0cjNva2UiLCJ0b2tlbiI6eyJpdiI6IjFhMzFlMzU5ZWU5ZDgwODcxZjg3NTkyYTg2NWIyYWY0IiwiY29udGVudCI6ImFkYjM1MjllNzdmNTcwNDBiNTRmZDVlNjQwZTkyN2Y4MWUyNjU1YWU4MjMwYmM2YTljNTYwZjhkNzU3NzBmYTVkZWY1MTZlZTQ1MGI0OWUyMjQxY2FmYjhjZGU5YjgyMjZlMzBiMjhhOTM1NjNjMjIzOGRlZjY4YTFlYjk0YjY0MWNmYzRjM2FjYjEyZjgwMjlkN2M4NDA3YmE4N2NkMjdkMTZjOGY5ODdiZTFlODIxN2EyNjAyNzk5NGYxNTYyOTI1MzI2MGQxNmZmNmM4ZDIwZjg4ZWIwZTY3Yjk1NDRiZGUwYzgxODY5ODliMDUzMmRkNTQwZjNkYTNhMmMzOWY0OGJjOTljNDc2ZTY1NWYzYmEwYTczYTUyMzg1YmU5MGI0MzYwYTQ5YWVmNzgyODA3MGVjOWE0ODhiOTBkY2FjYjNjMjcyN2MyN2VjMDc4NTNkOThiZWNiNzUzZjlkOTdmOWI0MDc4ZWE1N2M4NzhmNGY1ODQ5ZDAxYjM2OGU0ZmM1ZWJmMDU2NjY3OGFkNzBhMmQ5ZjgzYjllYTEyYmM5MTU3MDEzZjI4NDhhOGU5MThiZmQwMDg5MDMzZWM1Nzk1Mjc1ZjFjMjliYjRjZTg5YTk5NzU2MDk3YmQ2YjM1ZWRlZDQ0ZjI1ODAyMjQ3NWFiMjVhNmQ1M2RlNDE0YjE5YTk0ZjVmNDdhNTE5ZmUzMzdiMmU4NjJlZTdlMTk2ODI3ZTQwYzVmNDc3YmM3OGJhMGRlMGQzZmQ1MmY2NzA4Mjg1Njg2YmQ4NWM5ZTJmYTgxZTViNDE4MTkwMzZjZmQ3MzRjZDAxNWNmMmExMzcxMjIyNTkwZDQzN2EyMDNjZTk5MmJmY2I5ZWM3M2Q2OGQ3YzliMGM2In0sInNlY3VyaXR5VG9rZW4iOnsiaXYiOiIxYTMxZTM1OWVlOWQ4MDg3MWY4NzU5MmE4NjViMmFmNCIsImNvbnRlbnQiOiI4NTgwNGRhMTRmZjQ1MjczOGU3NmU4Zjc1OGE2MjVmZTFjN2Q2ZTk1OTMwZmI0MTVhYzIyMmU4YzE2NzYyZTk1YmNkYzA1YmQyODNiNzU5YzdjNGQ5NDg2In0sImp0aSI6IjU3ZjRhMWRjLTdkYzMtNDA0OC1hYmNmLTUzZGJmMzc5ZjVhOCIsImlhdCI6MTY5OTc3OTg4NiwiZXhwIjoxNjk5NzgzNDg1fQ.BwyWJidMD-R6yULqV_guIec__UtwojWGEvOV4Owm3E4"

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

    for fuelStation in fuelStationRawData['result'][:3]:
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
    for gasStation in gasStations:
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

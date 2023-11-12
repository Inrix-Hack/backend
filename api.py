import json
from time import sleep

import requests

apiToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcHBJZCI6InF0ZXQ0cjNva2UiLCJ0b2tlbiI6eyJpdiI6IjBjNGJkZWNjYmEzNGU0MTliNTc1NWE3NmIwMjA5N2E4IiwiY29udGVudCI6ImI4YjdmZThiNDcwMzc5NTY3NjI2Yjk5YWNjMWYyYjU3ODBlOWY4MmMwZmJjNDk0MGUyZjI3MWZjMjUzMjk0N2EzNjRlYWUwZDJjMWVmMmI0ZjBlZmFkNTM3OWE3ZDFiZTAwNjM1YWJmOTJiNTg3ZTkzNTJmYzRlMDRhODAzNjVmNzY4MzgxNTZmZDJjYzU5NDg2YWRjZmQ4ZWIyMmMyZjQ2N2RlYzdhNzk0ZjllZTc1OTMxMGY3MWE4MDA3OTM0OWI5NDZkODFkYTk4OTEzYWQyOWI1NzEzYWMxODlhNzc0MTY3MDhmYWJkMzIyMTdmYjczOWRkYzQ4OTAzMjAzMWE1M2I4MWFiNGM0ZTQyNzAyMGMwYTkwZDkwMjhiMWM1Mzg3NzMzOWRhMDk0Nzg3OTA1YWI5ZmU5OWQwMTFiN2UxNjJiZTUzNjc2MTc5MDhmNWQ0MmZiNDUxMTYwNDRlOWE3NWVkMTE5ZDQ3ODU5YmVkNDBmODU2YTRmMWI4ODYyYjc5N2I5YWVmMTkyNzNiMDNhMzQxODk1ZmMwYmNlN2EwNzM4YzAxODhiYjFlOTdkZWNiYTU1Yjg5MGZiNTUxNGJmMDlkMzEyOGIxNDkzNmVmYmUyMTRmNWQ3MDU1N2JiNTIyOTVjMTU5MmE3NjY0NmE0NmI5MjVmYWMyOTNhN2JhNTNiZDI3MDQ3MzIzMjc5ODU4NjkxOTRiY2I1NjIwMWQzNTdmNzg4N2Y1NTk5NzUyNWNjMmZkYmY1NDA0MWI1NDk2OGY4YWY5NDc0NmMwNTJjOWIyMjA3Mzc5ODNmYmU1MDlmMjA5NjliM2IzNTk0Zjk2MzQzYjg0MmJiNzAzN2YzY2Y5ZmExN2NlODg5ZTI5ZjBjYWEwIn0sInNlY3VyaXR5VG9rZW4iOnsiaXYiOiIwYzRiZGVjY2JhMzRlNDE5YjU3NTVhNzZiMDIwOTdhOCIsImNvbnRlbnQiOiJhYmZiZGRhODRkMGYyYTRjNWQxOWE5YjdjOTI4MGEyMTg1YjJmZDNlNzI5NDU2MTNlOGViMDE5ODFhMGQ5ZDZiMzM2ZmEzNzI3NjM4Y2NjZGMyYmFhYzZkIn0sImp0aSI6IjJlYWJmMGFlLWFjMjEtNDUyOC1iNWQ5LTg2NmY5ZmJiZDA0NSIsImlhdCI6MTY5OTc5NjM0NSwiZXhwIjoxNjk5Nzk5OTQ1fQ.ukuoCegEbaJoWVNG0EdlIOWjSDG0Wh9HV5sOR39rG50"

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
        route = response.json()['result']['trip']['routes'][0]

        stations.append([route['id'], gasStation, ((float(route['totalDistance']) / mpgOfCar * 2) + (
                    maximumCapacityOfCar - currentFuelInCar)) * stationPrice, float(route['totalDistance']),
                         float(route['travelTimeMinutes']), distance/mpgOfCar])
    stations.sort(key=lambda x: x[2])

    return [{
        "route": station[0],
        "coordinates": station[1]['coordinates'],
        "totalCost": station[2],
        "distance": station[3],
        "gallonsConsumed": station[4],
    } for station in stations[:3]]

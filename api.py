import json
from time import sleep

import requests

apiToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcHBJZCI6InF0ZXQ0cjNva2UiLCJ0b2tlbiI6eyJpdiI6IjA1ZDgxNDg5MzVlN2FkZmEzMjFmZDlkODJmNjJhZmNlIiwiY29udGVudCI6ImM2YzZkODdiZGYxZDBkNGRmMzk2NDhlNDQxOTc0YzMzYzhkNjBhOGM5NTE2YzA2MjdhMTZmMDQ3ZjgzZGI4NDFmNzQ5MzlhNjNiNTczNzRhMDc4MDhmZmM1ZGQ5YmQyM2RhNGIzZmU5ZWExOWEwOTBlNjhkMDZjYzQ2Y2VkNzFkYWUzZTM0Njk5NDNmOTAyZGMyN2FmZjk0YjQ1M2FhZTI3N2JjYzk3NTk4NTFiZDY4MDBiZWQwOTFmNTBkMDgwYjQ0MGY5YTlkYWZhZjU3ZmM3MzJlODBiODEyYTI3NTM4MTI2ZWI4NDdlN2Q0MGQ0Zjk1MDg4NzA5MDdhOWYyNjE2ZGMyNjNjYzE4NTgyODkzMTVlOGU3ZTg3MmQzYWQ2YWIyODgzNDZiMTdhNDMxZmZmODkxZDUwYzc3NDkwZjk0NDhjYWVjMmJiODFjNWQ1OWQ0NTYxOTM0MGVkMThiYzVjNTJiMzMyNTkzNmE0NzhiZGMxNzQyZjMxYWI1MDIyMTIzYTMzMmI3YThiMGM3YjQ4Zjg4ZTA1YzAwODMyMjYwYWVkYjQzNDU2MmQ0NjBkMTBiNjg1ZWEyZDQxZmI5MWUxZTJhODdlOTdhNDliZmJiY2EwZDQ3Yzk0NzhlMmVkYzliMjY1MDU2OWJiMWUxNDVkM2FhN2Q4MTRhYjcyOGVlMDdmYTExMWE3YjMwOGNiOTc4MmVlODRmMWJmZjYxYTRiMjZkMzZhNmQ4ODgzYzBjYWEyNDljZGUyMmJlYWI3MDJjMjc5MTAyYjI5MTk5ZTVkODdmMTA0ODRiZGY5ZDMzZmRjZjkxZmY5NDY3Mzk1YTliZDJlZjI1YzQ4NDU1MzEzOTllN2VmZGIxYmRhNzZmMzkifSwic2VjdXJpdHlUb2tlbiI6eyJpdiI6IjA1ZDgxNDg5MzVlN2FkZmEzMjFmZDlkODJmNjJhZmNlIiwiY29udGVudCI6IjliZjRlNjc2ZjMxMzBhMTJmMWE4NmZlYzUzYTY0YTU3YjA4ODI1YmI4NDBkZjgxNTQzNjFlYTQyZjM2M2I5MzRkNjU4MTZkNDczNTQ3OTY3NWViNmYzYzIifSwianRpIjoiZGZjYmRiY2EtZTFiNy00YzFhLWE1ZmMtOTQ2ZGUzNTZiY2U1IiwiaWF0IjoxNjk5ODAwNjA3LCJleHAiOjE2OTk4MDQyMDd9.cQF6CtETQfwSI8CWmgjv1FfgP--nyou8KEThMrViBhE"

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

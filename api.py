import json
from time import sleep

import requests

apiToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcHBJZCI6InF0ZXQ0cjNva2UiLCJ0b2tlbiI6eyJpdiI6ImJkYzFjYWRlNTQzOWI4ZDEwNDYzMjg1MTkzZDQ1ODUxIiwiY29udGVudCI6ImY5NDU0M2FmOWY2YWQ2MWQ2MjEzMmRjYWRhOWNkY2Y2M2M0ODE5NDJlMGU3NDMyYzNlMzNiZDMwZTVhZjFiNDhkMzVlZDRmOGE4MzE4NmNiNmE5NTc0ZGQxYmQ4MGQ2NTAzODIwYzE5YTA1ODc1ZTUxMzgzYTQ0NTA0MWMwMzIyNjAzMzBjMDI0NjczYmJhYTBjYjM1MzMxZTE2ODcxOTk4YWZkYmEyZDllNjE3NTBmMjM5OWZiN2JmN2VhNDQzNGZjMjFkMzgzMzVmMzY1YmEzMzkyNjQ3Y2FmYjFhMDk2MjNkMDQ2NDhmMThiMTYwMGM2NWUxOTJmZGU0YzVkOWFhMDljZWRhOTgyZTVjMTQwMmNiYzJlZmUyODAyZTgzOWNhMTE3YmJmM2MwNTlkZWQ3YmEzZTgyZWE1MGRlYjM4ZGQyMGI0Y2Q1N2E5NWUyNjgzYTc5NTA0YzQ0ZWE4Y2YxMDMxYzQ3MDU1MjkyMzAxYjlhNWY1ZjM2M2JkYzFjNTA5NTdkNTI0ZGMzMDA2MTNjNGU4ODhiZjViYTc0ZTJjNzU3MzExZjM5OWYyODE3MjRmNGYwOGRhZDM2NmE0YzY4YjJmODc3MjIyNjJkNjYxYzdhZTFlZDljNDRlNTFjNjg0OTM0MDA3MThkYWViOGY2ZWMwMTc0YWM4MjM4YzNiMGExZTI3ZmQ3ZmNhMThkNjVjMjg2ZGVmNjY0YjhmMTk3ODc5YTc4YjNiM2U4ODVhYzVhM2FhNjFiZWU5Nzk1OGIzMTNjNGE0ODA3M2I4MTI1NzIxNjVlYzlmMjkwYWQ5YzQ0NzMzY2JmNWUwMGVjYTI0OTQwNTRiZjY4ZDg3NzYxZGU1YzhkZGM1YTU4MTZmNGIxNDQzIn0sInNlY3VyaXR5VG9rZW4iOnsiaXYiOiJiZGMxY2FkZTU0MzliOGQxMDQ2MzI4NTE5M2Q0NTg1MSIsImNvbnRlbnQiOiJjNjc4NzFiMGE4NDc4MjI2NWYxODEwYWViOGI3ZDZiZjQ3NzQ2MDYyOWZlMzRiNTAzYzI3YzM0MGZhYWMxODQxZjE0NGVhODJlZTAxYTZkMTM3Yzc1M2UzIn0sImp0aSI6ImU5NjRhZWNlLWYxMDItNDRiMC1iOTM0LWRmMjBkNWVjZDExZCIsImlhdCI6MTY5OTc4ODU3NCwiZXhwIjoxNjk5NzkyMTc0fQ.xC2LqVO3oJTEnNPX2fu5f4APu2S-In0BLr09s8Y1Gvk"

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

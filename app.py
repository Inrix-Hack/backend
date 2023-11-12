from flask import Flask, make_response
from api import getFuelStations, getRoutes

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/fuelStations')
def get_incidents():
    response = make_response(getFuelStations())
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/routes')
def get_routes():
    currentFuelInCar = 10
    mpgOfCar = 20
    maximumCapacityOfCar = 20
    fuelStations = getFuelStations()
    # return str(len(fuelStations))
    response = make_response(getRoutes(fuelStations, currentFuelInCar, mpgOfCar, maximumCapacityOfCar))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == '__main__':
    app.run()

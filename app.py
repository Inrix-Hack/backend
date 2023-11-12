from flask import Flask, make_response
from api import getFuelStations, getRoutes

app = Flask(__name__)


@app.route('/fuelStations')
def get_incidents():
    response = make_response(getFuelStations())
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/routes')
def get_routes():
    response = getRoutes()
    response = make_response(getFuelStations())
    response.headers['Access-Control-Allow-Origin'] = '*'


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()

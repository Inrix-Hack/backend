from flask import Flask
from api import getIncident, getRoutes

app = Flask(__name__)


@app.route('/incidents')
def get_incidents():
    return getIncident()

@app.route('/routes')
def get_routes():
    return getRoutes()

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()

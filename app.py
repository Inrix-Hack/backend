from flask import Flask, make_response
from api import getIncident

app = Flask(__name__)


@app.route('/incidents')
def get_incidents():
    response = make_response(getIncident())
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()

from flask import Flask
from setup import Setup

app = Flask(__name__)


@app.route('/task1')
def hello_world():
    se = Setup()
    se.initialize_clients()
    return "success"


if __name__ == '__main__':
    app.run(debug=True, port=1111)

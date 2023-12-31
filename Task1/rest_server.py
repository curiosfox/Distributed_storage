import logging
import subprocess
import sys

from flask import Flask, app, request

from Distributed_storage.Task1.server import Server

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route('/')
def hello():
    return "Welcome to Distributed Storage Project"


@app.route('/task1', methods=["POST"])
def task1():
    params_json = request.get_json()
    server_obj = Server(nodes=params_json.get('nodes', 4), operation=params_json.get('operation', 'random'),
                        file_size=params_json.get('file_size', 100 * 1024), repeat=params_json.get("repeat", 100))
    server_obj.task1_single_process()
    with open('result.json') as file:
        return file.read()


@app.route('/task2', methods=["POST"])
def task2():
    params_json = request.get_json()
    server_obj = Server(nodes=params_json.get('nodes', 4), operation=params_json.get('operation', 'random'))
    server_obj.task2_single_process()
    with open('result.json') as file:
        return file.read()


if __name__ == "__main__":
    app.run(debug=True)

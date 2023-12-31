import logging
import subprocess
import sys

from flask import Flask, app, request

from Distributed_storage.Task2.server import Server

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route('/')
def hello():
    return "Welcome to Distributed Storage Project"


@app.route('/task1', methods=["POST"])
def task1():
    valid_argument = ["repeat", "file_size", "nodes", "operation"]
    default_value = {
        "repeat": 100,
        "file_size": 100 * 1024,  # 100kb
        "nodes": 4,
        "operation": "random"
    }
    command_line = ""
    for argument in valid_argument:
        if argument in request.form:
            command_line += f"--{argument} {request.form[argument]} "
        else:
            command_line += f"--{argument} {default_value[argument]} "
    logging.info(f"Command line generated :{command_line}")
    subprocess.run([sys.executable, "Task1/server.py"], check=True)
    with open('../Task1/result.json') as file:
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

import os
import logging
from copy import deepcopy

import zmq


class Client(object):
    def __init__(self, env_port):
        logging.basicConfig(level=logging.INFO)
        self.client_name = f"client{int(env_port) - 5554}"
        self.ledger = list()

    def start_client(self):
        context = zmq.Context()
        socket = context.socket(zmq.DEALER)
        socket.setsockopt(zmq.RATE, 5 * 1000)
        socket.connect(f"tcp://host.docker.internal:{port}")
        logging.info(f"running on port :{port}")
        data_str = {
            "identity": self.client_name,
            "data": f"{self.client_name} Connecting"
        }
        socket.send_json(data_str)
        return socket

    def check_file_duplicates(self, file_name, fragment):
        for ledger_log in self.ledger:
            if ledger_log["file_name"] == file_name and ledger_log["fragment"] == fragment:
                return True
        else:
            return False

    def handle_operations(self, socket):
        while True:
            rec_json = socket.recv_json()
            logging.info(rec_json)
            if rec_json["identity"] == self.client_name:
                logging.info(f"Received operation:{rec_json['operation']}")
                if rec_json['operation'] == "store":
                    file_name = rec_json['file_name']
                    fragment = rec_json['fragment']
                    ledger_log = {
                        "file_name": file_name,
                        "fragment": fragment
                    }
                    self.ledger.append(deepcopy(ledger_log))
                    with open(f"{rec_json['file_name']}_fragment{rec_json['fragment']}", "w") as file:
                        file.write(rec_json["data"])
                elif rec_json['operation'] == "load":
                    with open(f"{rec_json['file_name']}_fragment{rec_json['fragment']}", "r") as file:
                        content = file.read()
                    send_json = {
                        "file_name": rec_json['file_name'],
                        "fragment": rec_json['fragment'],
                        "data": content
                    }
                    socket.send_json(send_json)
                else:
                    send_json = {
                        "data": f"Operation Heartbeat"
                    }
                    socket.send_json(send_json)

    def automate_task1(self):
        socket = self.start_client()
        self.handle_operations(socket)


if __name__ == "__main__":
    port = os.environ.get("PORT")
    client_obj = Client(port)
    client_obj.automate_task1()

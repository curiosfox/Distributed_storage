import os
import logging
import zmq


def client(port, message):
    logging.basicConfig(level=logging.DEBUG)
    client_name = f"client{int(port) - 5554}"
    context = zmq.Context()
    socket = context.socket(zmq.DEALER)
    socket.connect(f"tcp://host.docker.internal:{port}")
    logging.info(f"running on port :{port}")
    data_str = {
        "identity": client_name,
        "data": message
    }
    socket.send_json(data_str)
    while True:
        # Receive response from server
        rec_json = socket.recv_json()
        logging.info(rec_json)
        if rec_json["identity"] == client_name:
            logging.info(f"Received operation:{rec_json['operation']}")
            if rec_json['operation'] == "store":
                with open(f"{rec_json['file_name']}_fragment{rec_json['fragment']}", "w") as file:
                    file.write(rec_json["data"])
            if rec_json['operation'] == "load":
                with open(f"{rec_json['file_name']}_fragment{rec_json['fragment']}", "r") as file:
                    content = file.read()
                send_json = {
                    "file_name": rec_json['file_name'],
                    "fragment": rec_json['fragment'],
                    "data": content
                }
                socket.send_json(send_json)


if __name__ == "__main__":
    port = os.environ.get("PORT")
    client_message = "Hello World!!!!"
    client(port, client_message)

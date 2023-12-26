import os

import zmq


def client(port, message):
    client_name = "client1"
    context = zmq.Context()
    socket = context.socket(zmq.DEALER)
    socket.connect(f"tcp://mynet:{port}")
    print(f"running on port :{port}")
    data_str = {
        "identity": client_name,
        "data": message
    }
    socket.send_json(data_str)
    while True:
        # Receive response from server
        rec_json = socket.recv_json()
        print(rec_json)
        if rec_json["identity"] == client_name:
            print(f"Received operation:{rec_json['operation']}")
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

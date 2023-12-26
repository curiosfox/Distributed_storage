import zmq


def client(port, message):
    client_name = "client2"
    context = zmq.Context()
    socket = context.socket(zmq.DEALER)
    socket.connect(f"tcp://localhost:{port}")

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
            print(f"Received operation:{rec_json['operation']}\n Data:{rec_json['data']}")
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
    port = 5555
    client_message = "Hello World!!!!"
    client(port, client_message)

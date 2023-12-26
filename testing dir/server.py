import random

import zmq
from FileOperations import FileOps
from FileDistribution import FileDistribution


def server(port):
    context = zmq.Context()
    socket = context.socket(zmq.DEALER)
    socket.bind(f"tcp://*:{port}")
    print(f"Server listening on port {port}")
    ledger = dict()
    file_name = "testing.txt"
    connected_clients = []
    while len(connected_clients) < 4:
        rec_json = socket.recv_json()
        identity = rec_json["identity"]
        message = rec_json["data"]
        # Check if client is already connected
        if identity not in connected_clients:
            connected_clients.append(identity)
            print("Client connected:", identity)
            break
    print("All clients connected")
    fileops = FileOps(1024)
    file_dist = FileDistribution(len(connected_clients))
    fragments = fileops.generate_and_fragment_file(file_name, 4)
    placements = file_dist.random_placement(fragments)
    ledger[file_name] = list()
    for placement in placements:
        ledger[file_name].append({
            "client_name": placement['client_name'],
            "fragment": placement["fragment_number"]
        })
    for placement in placements:
        print(f"Sending file to: {placement['client_name']} fragement :{placement['fragment_number']}")
        # Send the message to the specified client
        final_json = {
            "identity": placement['client_name'],
            "operation": "store",
            "data": placement["data"],
            "fragment": placement["fragment_number"]
        }
        socket.send_json(final_json)
    file_fragments = []
    for data_entry in ledger[file_name]:
        load_json = {
            "identity": data_entry['client_name'],
            "operation": "load",
            "fragment": data_entry['fragment']
        }
        socket.send_json(load_json)
        file_fragments.insert(data_entry['fragment'], socket.recv_json()["data"])

if __name__ == "__main__":
    port = 5555
    server(port)

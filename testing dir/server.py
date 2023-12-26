import random
from copy import deepcopy
from time import sleep

import zmq
from FileOperations import FileOps
from FileDistribution import FileDistribution


def server(port, nodes=4):
    context = zmq.Context()
    socket_list = list()
    for node in range(nodes):
        socket = context.socket(zmq.DEALER)
        socket.bind(f"tcp://*:{port + node}")
        socket_list.append(socket)
        print(f"Server listening on port {port + node}")
    ledger = dict()
    file_name = "testing.txt"
    connected_clients = dict()
    for socket_cli in socket_list:
        rec_json = socket_cli.recv_json()
        identity = rec_json["identity"]
        # Check if client is already connected
        if identity not in connected_clients:
            connected_clients[identity] = socket_cli
            print("Client connected:", identity)
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
            'file_name': file_name,
            "operation": "store",
            "data": placement["data"],
            "fragment": placement["fragment_number"]
        }
        connected_clients[placement['client_name']].send_json(final_json)
    file_fragments = []
    print("All files fragments sent")
    for data_entry in ledger[file_name]:
        print(f"loading file from :{data_entry['client_name']}")
        load_json = {
            "identity": data_entry['client_name'],
            'file_name': file_name,
            "operation": "load",
            "fragment": data_entry['fragment']
        }
        connected_clients[data_entry['client_name']].send_json(load_json)
        file_fragments.insert(data_entry['fragment'], connected_clients[data_entry['client_name']].recv_json()["data"])
    data = fileops.combine_fragments(file_fragments)
    print(fileops.compare_files(fileops.read_file(file_name), data))


if __name__ == "__main__":
    port = 5555
    server(port)

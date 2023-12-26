from copy import deepcopy

import zmq


class ServerNode(object):

    def __init__(self, nodes):
        self.nodes = nodes
        self.port = 5555
        self.socket_list = list()
        context = zmq.Context()
        for node in range(0, nodes):
            socket = context.socket(zmq.DEALER)
            socket.bind(f"tcp://*:{self.port + node}")
            print(f"Server listening on port {self.port + node}")
            self.socket_list.append(deepcopy(socket))

    def connect_clients(self):
        connected_clients = list()
        for socket in self.socket_list:
            rec_json = socket.recv_json()
            identity = rec_json["identity"]
            message = rec_json["data"]
            if identity not in connected_clients:
                connected_clients.append(identity)
                print("Client connected:", identity)
        print("All clients connected")

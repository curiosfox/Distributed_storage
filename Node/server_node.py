import os

import retry
import zmq
import time


class Server(object):

    def __init__(self):
        self.name = f"server_{os.name}"

    def generate_file(self, name, size):
        file_path = f"{os.path.join(name)}"
        with open(file_path, 'wb') as file:
            file.truncate(size)
        print(f"File generated in :{file_path} with size (in bytes):{size}")
        return file_path

    @retry(exceptions=Exception, tries=10, delay=1)
    def get_all_clients_connected(self, n=4):
        clients_list = list()
        for i in range(0, n):
            client_socket, conn = self.socket.recv_multipart()
            print(f"Obtained client :{conn}")
            clients_list.append(client_socket)
        if len(clients_list) < n:
            raise Exception(f"Client list not fully updated :{clients_list}")
        return clients_list

    def start_server(self):
        print(f"Starting Server :{self.name}")
        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind("tcp://*:5555")
        start = time.time()

        while (time.time() - start < 10):
            clients_connected = self.get_all_clients_connected()
        while True:
            self.generate_file("test", 1024 * 1024)

            message = self.socket.recv()

            #  Do some 'work'
            time.sleep(1)

            #  Send reply back to client
            self.socket.send(b"World")


if __name__ == "__main__":
    server = Server()
    server.start_server()

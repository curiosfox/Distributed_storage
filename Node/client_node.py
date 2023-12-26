import logging as log
import os
import zmq


class Client(object):
    def __init__(self):
        self.name = f"Client_{int(open('port.txt', 'r').read()) - 5555}"
        self.port = int(open('port.txt', 'r').read())

    def start_client(self):
        print(f"Starting client:{self.name}")
        context = zmq.Context()
        #  Socket to talk to server
        print("Connecting to hello world server…")
        socket = context.socket(zmq.REQ)
        socket.connect(f"tcp://localhost:{self.port}")

        #  Do 10 requests, waiting each time for a response
        for request in range(10):
            print(f"Sending request {request} …")
            socket.send(b"Hello")

            #  Get the reply.
            message = socket.recv()
            print(f"Received reply {request} [ {message} ]")


if __name__ == "__main__":
    client = Client()
    client.start_client()

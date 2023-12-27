import argparse
import subprocess

import zmq
import docker
from FileOperations import FileOps
from FileDistribution import FileDistribution
from docker_deploy import DockerDeployment
import logging
import sys


class Server(object):
    def __init__(self, port=5555, nodes=4, file_size=1024, throttle=0, fragments=4, operation="random",
                 repeat=1, **kwargs):
        self.ledger = None
        self.port = kwargs.get('port', 5555)
        self.nodes = kwargs.get('nodes', 4)
        self.file_size = kwargs.get('file_size', 1024)
        self.throttle_bandwidth = kwargs.get('throttle', 0)
        self.fragments = kwargs.get('fragments', 4)
        self.operation = kwargs.get('operation', "random")
        self.repeat = kwargs.get('repeat', 1)
        logging.basicConfig(level=logging.DEBUG)

    def start_server(self):
        context = zmq.Context()
        socket_list = list()
        for node in range(self.nodes):
            socket = context.socket(zmq.DEALER)
            socket.bind(f"tcp://*:{self.port + node}")
            socket_list.append(socket)
            logging.info(f"Server listening on port {self.port + node}")
        return socket_list

    def deploy_client_nodes(self):
        docker_deployment = DockerDeployment()
        yaml_file = docker_deployment.generate_yml_file(nodes=self.nodes)
        client = docker.from_env()
        try:
            # Build and start Docker Compose services
            subprocess.run(['docker-compose', '-f', yaml_file, 'up', '-d'], check=True)
            logging.info("Docker Compose deployment successful.")
        except Exception as e:
            logging.error(f"Error deploying Docker Compose: {e}")

    def connect_all_clients(self, socket_list):
        connected_clients = dict()
        for socket_cli in socket_list:
            logging.info(f"Trying on the socker{socket_cli}")
            rec_json = socket_cli.recv_json()
            identity = rec_json["identity"]
            connected_clients[identity] = socket_cli
            logging.info(f"Client connected:{identity}")
        logging.info("All clients connected")
        return connected_clients

    def get_placement(self, connected_clients, file_name):
        self.fileops = FileOps(self.file_size)
        file_dist = FileDistribution(len(connected_clients))
        fragments = self.fileops.generate_and_fragment_file(file_name, self.fragments)
        operation_dict = {
            "random": file_dist.random_placement,
            "buddy": file_dist.buddy_approach_placement,
            "min_copy": file_dist.min_copysets_placement,
        }
        return operation_dict[self.operation](fragments)

    def store_file_in_clients(self, connected_clients, placements, file_name):
        self.ledger = dict()
        self.ledger[file_name] = list()
        for placement in placements:
            self.ledger[file_name].append({
                "client_name": placement['client_name'],
                "fragment": placement["fragment_number"]
            })
        for placement in placements:
            logging.info(f"Sending file to: {placement['client_name']} fragement :{placement['fragment_number']}")
            # Send the message to the specified client
            final_json = {
                "identity": placement['client_name'],
                'file_name': file_name,
                "operation": "store",
                "data": placement["data"],
                "fragment": placement["fragment_number"]
            }
            connected_clients[placement['client_name']].send_json(final_json)

    def load_file_from_clients(self, connected_clients, file_name):
        file_fragments = []
        logging.info("All files fragments sent")
        for data_entry in self.ledger[file_name]:
            logging.info(f"loading file from :{data_entry['client_name']}")
            load_json = {
                "identity": data_entry['client_name'],
                'file_name': file_name,
                "operation": "load",
                "fragment": data_entry['fragment']
            }
            connected_clients[data_entry['client_name']].send_json(load_json)
            file_fragments.insert(data_entry['fragment'],
                                  connected_clients[data_entry['client_name']].recv_json()["data"])
        return file_fragments

    def validate_file(self, fragaments, file_name):
        data = self.fileops.combine_fragments(fragaments)
        return self.fileops.compare_files(self.fileops.read_file(file_name), data)

    def task1_single_process(self, file_name="testing.txt"):
        socket_list = self.start_server()
        self.deploy_client_nodes()
        connected_clients = self.connect_all_clients(socket_list)
        placements = self.get_placement(connected_clients, file_name=file_name)
        self.store_file_in_clients(connected_clients, placements, file_name)
        fragments = self.load_file_from_clients(connected_clients, file_name)
        logging.info(self.validate_file(fragments, file_name))


def server(port, nodes=4):
    logging.basicConfig(level=logging.DEBUG)
    context = zmq.Context()
    socket_list = list()
    for node in range(nodes):
        socket = context.socket(zmq.DEALER)
        socket.bind(f"tcp://*:{port + node}")
        socket_list.append(socket)
        logging.info(f"Server listening on port {port + node}")
    ledger = dict()
    file_name = "testing.txt"
    connected_clients = dict()
    for socket_cli in socket_list:
        logging.info(f"Trying on the socker{socket_cli}")
        rec_json = socket_cli.recv_json()
        identity = rec_json["identity"]
        connected_clients[identity] = socket_cli
        logging.info(f"Client connected:{identity}")
    logging.info("All clients connected")
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
        logging.info(f"Sending file to: {placement['client_name']} fragement :{placement['fragment_number']}")
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
    logging.info("All files fragments sent")
    for data_entry in ledger[file_name]:
        logging.info(f"loading file from :{data_entry['client_name']}")
        load_json = {
            "identity": data_entry['client_name'],
            'file_name': file_name,
            "operation": "load",
            "fragment": data_entry['fragment']
        }
        connected_clients[data_entry['client_name']].send_json(load_json)
        file_fragments.insert(data_entry['fragment'], connected_clients[data_entry['client_name']].recv_json()["data"])
    data = fileops.combine_fragments(file_fragments)
    logging.info(fileops.compare_files(fileops.read_file(file_name), data))


class SysArgument(object):
    @staticmethod
    def parse_arguments():
        parser = argparse.ArgumentParser(description='Example script with command-line arguments')
        parser.add_argument('--repeat', type=int, help='Number of times to repeat the operation')
        parser.add_argument('--file_size', type=int, help='The size of the file in Bytes')
        parser.add_argument('--nodes', type=int, help='Number of Client Nodes to be deployed')
        parser.add_argument('--throttle', type=int, help='To throttle bandwidth')
        parser.add_argument('--fragments', type=int, help='Number of fragments to be generated per file')
        parser.add_argument('--operation', type=str,
                            help='Type of operation to be taken place while storing \n  '
                                 'Valid types : random \nbuddy\nmin_copy')

        args = parser.parse_args()
        return args


if __name__ == "__main__":
    arguments = vars(SysArgument.parse_arguments())
    server_obj = Server(**arguments)
    server_obj.task1_single_process()

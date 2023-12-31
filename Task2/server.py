import argparse
import subprocess
from copy import deepcopy

import zmq
import logging

from Distributed_storage.Task2.DockerSwarmManager import DockerSwarmManager
from Distributed_storage.Task2.FileOperations import FileOps
from Distributed_storage.Task2.FileDistribution import FileDistribution
from Distributed_storage.Task2.docker_deploy import DockerDeployment


class Server(object):
    def __init__(self, **kwargs):
        self.fileops = None
        self.ledger = dict()
        self.docker = DockerSwarmManager()
        self.port = 5555 if kwargs.get('port') is None else kwargs.get('port')
        self.nodes = 4 if kwargs.get('nodes') is None else kwargs.get('nodes')
        self.replicas = 3 if kwargs.get('replicas') is None else kwargs.get('replicas')
        self.file_size = 1024 if kwargs.get('file_size') is None else kwargs.get('file_size')
        self.throttle_bandwidth = 5000 if kwargs.get('throttle') is None else kwargs.get('throttle')
        self.fragments = 4 if kwargs.get('fragments') is None else kwargs.get('fragments')
        self.operation = "random" if kwargs.get('operation') is None else kwargs.get('operation')
        self.repeat = 1 if kwargs.get('repeat') is None else kwargs.get('repeat')
        logging.basicConfig(level=logging.DEBUG)

    def start_server(self):
        context = zmq.Context()
        socket_list = list()
        for node in range(self.nodes):
            socket = context.socket(zmq.DEALER)
            socket.bind(f"tcp://*:{self.port + node}")
            socket_list.append(socket)
            socket.setsockopt(zmq.RATE, 5 * 1000)  # 5Mb Rate
            logging.info(f"Server listening on port {self.port + node}")
        return socket_list

    def deploy_client_nodes(self):
        docker_deployment = DockerDeployment()
        yaml_file = docker_deployment.generate_yml_file(nodes=self.nodes)
        try:
            # Build and start Docker Compose services
            subprocess.run(['docker-compose', '-f', yaml_file, 'up', '-d'], check=True)
            logging.info("Docker Compose deployment successful.")
        except Exception as e:
            logging.error(f"Error deploying Docker Compose: {e}")

    @staticmethod
    def connect_all_clients(socket_list):
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
        return operation_dict[self.operation](fragments, replicas=self.replicas)

    def store_file_in_clients(self, connected_clients, placements, file_name):
        self.ledger[file_name] = list()
        for placement in placements:
            self.ledger[file_name].append({
                "client_name": placement['client_name'],
                "fragment": placement["fragment"],
                "replicas": placement["replica"]
            })
        for placement in placements:
            logging.info(f"Sending file to: {placement['client_name']} fragment :{placement['fragment']}")
            # Send the message to the specified client
            final_json = {
                "identity": placement['client_name'],
                'file_name': file_name,
                "operation": "store",
                "data": placement["data"],
                "fragment": placement["fragment"]
            }
            connected_clients[placement['client_name']].send_json(final_json)

    @staticmethod
    def get_file_fragments_for_given_replica(ledger, replica=1):
        final_fragment_list = list()
        for log_data in ledger:
            if log_data["replicas"] == replica:
                final_fragment_list.append(deepcopy(log_data))
        return final_fragment_list

    def load_file_from_clients(self, connected_clients, file_name):
        file_fragments = []
        logging.info("All files fragments sent")
        data_list = self.get_file_fragments_for_given_replica(self.ledger[file_name])
        logging.info(f"Get the list of clients for data:{data_list}")
        for data_entry in data_list:
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

    @staticmethod
    def heartbeat_collection(connected_clients):
        failed_heartbeat = list()
        for client_name, socket in connected_clients.items():
            logging.info(f"Checking for heartbeat in client :{client_name}")
            heartbeat_json = {
                'identity': client_name,
                'operation': 'heartbeat'
            }
            try:
                socket.send_json(heartbeat_json, flags=zmq.NOBLOCK)
                if socket.poll(2000, zmq.POLLIN):
                    logging.info("got message ", socket.recv_json(zmq.NOBLOCK))
                else:
                    logging.error("error: message timeout")
            except Exception as ex:
                logging.error(f"Obtained error on heartbeat request for client:{client_name}")
                failed_heartbeat.append(client_name)
        return failed_heartbeat

    def check_damage(self, failed_clients):
        damaged_files = list()
        fragment_lost = 0
        for file_name, file_ledger in self.ledger.items():
            refined_frag_list = list()
            for file_entry in file_ledger:
                if file_entry["client_name"] in failed_clients:
                    fragment_lost += 1
                else:
                    refined_frag_list.append(file_entry)
            # check if the files are intact
            fragment_checklist = [1, 2, 3, 4]
            for remain_filefrag in refined_frag_list:
                if remain_filefrag["fragment"] in fragment_checklist:
                    fragment_checklist.remove(remain_filefrag["fragment"])
            if len(fragment_checklist) != 0:
                damaged_files.append(file_name)
        return {
            "damaged files": damaged_files,
            "number of damaged_files": len(damaged_files),
            "number of fragments lost": fragment_lost
        }

    def cleanup(self, socket_list, directory_path):
        try:
            # Run Docker Compose down using subprocess
            subprocess.run(['docker-compose', 'down'], check=True)
            logging.info("Docker Compose cleanup successful.")
        except subprocess.CalledProcessError as e:
            logging.info(f"Error during Docker Compose cleanup: {e}")
        for socket in socket_list:
            socket.close()
        self.fileops.remove_directory(directory_path)

    def task2_single_process(self):
        file_dir_name = "file_dir"
        result_json = dict()
        socket_list = self.start_server()
        self.deploy_client_nodes()
        connected_clients = self.connect_all_clients(socket_list)
        file_list = FileOps.generate_files("file_dir", 100 * 1024)  # 100kb files
        for file in file_list:
            placements = self.get_placement(connected_clients, file_name=file)
            self.store_file_in_clients(connected_clients, placements, file)
        self.docker.random_kill_containers(num_containers_to_kill=2)
        failed_heartbeat = self.heartbeat_collection(connected_clients)
        result_json["2"] = self.check_damage(failed_heartbeat)
        self.docker.random_kill_containers(num_containers_to_kill=1)  # 3
        failed_heartbeat = self.heartbeat_collection(connected_clients)
        result_json["3"] = self.check_damage(failed_heartbeat)
        self.docker.random_kill_containers(num_containers_to_kill=1)  # 4
        failed_heartbeat = self.heartbeat_collection(connected_clients)
        result_json["4"] = self.check_damage(failed_heartbeat)
        self.docker.random_kill_containers(num_containers_to_kill=2)  # 6
        failed_heartbeat = self.heartbeat_collection(connected_clients)
        result_json["6"] = self.check_damage(failed_heartbeat)
        self.docker.random_kill_containers(num_containers_to_kill=2)  # 8
        failed_heartbeat = self.heartbeat_collection(connected_clients)
        result_json["8"] = self.check_damage(failed_heartbeat)
        self.docker.random_kill_containers(num_containers_to_kill=2)  # 10
        failed_heartbeat = self.heartbeat_collection(connected_clients)
        result_json["10"] = self.check_damage(failed_heartbeat)
        logging.critical(result_json)
        with open('result.json', 'w') as file:
            file.write(result_json.__str__())
        self.cleanup(socket_list, file_dir_name)


class SysArgument(object):
    @staticmethod
    def parse_arguments():
        parser = argparse.ArgumentParser(description='Example script with command-line arguments')
        parser.add_argument('--repeat', type=int, help='Number of times to repeat the operation')
        parser.add_argument('--replicas', type=int, help='Number of replicas to be generated for the file')
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
    server_obj.task2_single_process()

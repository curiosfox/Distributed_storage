import logging

import docker
import random


class DockerSwarmManager:
    def __init__(self):
        self.client = docker.from_env()

    def list_containers(self):
        try:
            containers = self.client.containers.list()
            return containers
        except Exception as e:
            print(f"Error listing containers: {e}")
            return []

    def random_kill_containers(self, num_containers_to_kill):
        try:
            all_containers = self.list_containers()
            client_containers = list()
            for container in all_containers:
                if 'client_node' in container.name:
                    client_containers.append(container)
            if len(client_containers) < num_containers_to_kill:
                print("Not enough containers in the Docker Swarm to kill.")
                return False

            containers_to_kill = random.sample(client_containers, num_containers_to_kill)
            for container in containers_to_kill:
                logging.info(f"{container.name} is killed")
                container.kill()
            print(f"{num_containers_to_kill} containers killed randomly in the Docker Swarm.")
            return True

        except docker.errors.APIError as e:
            print(f"Error killing containers in the Docker Swarm: {e}")
            return False

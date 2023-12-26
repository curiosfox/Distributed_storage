import yaml


class DockerDeployment(object):
    def generate_yml_file(self, nodes=4):
        # Define the base structure of the Docker Compose file
        docker_compose_data = {
            'version': '3.7',
            'services': {
                'network_switch': {
                    'image': 'alpine',
                    'command': 'tail -f /dev/null',
                    'networks': ['mynet']
                },
                'server_node': {
                    'image': 'python:3.8-alpine',
                    'depends_on': ['network_switch'],
                    'environment': {
                        "PORT": 5555,
                    },
                    'entrypoint': "sh -c 'pip3 install -r requirements.txt'",
                    'command': "sh -c 'python3 server.py'",
                    'networks': ['mynet'],
                    'volumes': ['./client.py:/server.py', './requirements.txt:/requirements.txt',
                                './FileDistribution.py:/FileDistribution.py', './FileOperations.py:/FileOperations.py']
                }
            },
            'networks': {
                'mynet': {'driver': 'bridge'}
            }
        }

        # Add client nodes to the Docker Compose file
        for i in range(0, nodes):
            client_name = f'client_node_{i}'
            docker_compose_data['services'][client_name] = {
                'image': 'python:3.8-alpine',
                'depends_on': ['network_switch'],
                'networks': ['mynet'],
                'environment': {
                    "PORT": f"{5555 + i}"
                },
                'entrypoint': "sh -c 'pip3 install -r requirements.txt'",
                'command': "sh -c 'python3 client.py'",
                'volumes': ['./client.py:/client.py', './requirements.txt:/requirements.txt',
                            './FileDistribution.py:/FileDistribution.py', './FileOperations.py:/FileOperations.py']
            }

            # Write the generated YAML data to a file
            with open('docker-compose.yml', 'w') as yaml_file:
                yaml.dump(docker_compose_data, yaml_file, default_flow_style=False)

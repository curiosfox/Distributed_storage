import yaml


class DockerDeployment(object):
    def generate_yml_file(self, nodes=4):
        docker_compose_data = {
            'version': '3.7',
            'services': {
                'network_switch': {
                    'image': 'alpine',
                    'command': 'tail -f /dev/null',
                    'networks': ['mynet']
                },
            },
            'networks': {
                'mynet': {'driver': 'bridge'
                          }
            }
        }

        # Add client nodes to the Docker Compose file
        for i in range(0, nodes):
            client_name = f'client_node_{i}'
            docker_compose_data['services'][client_name] = {
                'image': 'python:3.8-alpine',
                'depends_on': ['network_switch'],
                'environment': {
                    "PORT": f"{5555 + i}"
                },
                'networks': {
                    'mynet'
                },
                'ports': [f"{5555 + i}:{5555 + i}"],
                'command': "sh -c 'pip3 install -r requirements.txt && python3 client.py'",
                'volumes': ['./client.py:/client.py', './requirements.txt:/requirements.txt',
                            './FileDistribution.py:/FileDistribution.py', './FileOperations.py:/FileOperations.py']
            }

            # Write the generated YAML data to a file
            with open('docker-compose.yml', 'w') as yaml_file:
                yaml.dump(docker_compose_data, yaml_file, default_flow_style=False)

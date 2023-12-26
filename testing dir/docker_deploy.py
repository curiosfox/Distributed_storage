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
                'flask_server': {
                    'image': 'python:3.8-alpine',
                    'command': 'sh - c "pip3 install -r requirements.txt && python -m flask run --host=0.0.0.0"',
                    'ports': ['5000:5000'],
                    'depends_on': ['network_switch'],
                    'networks': ['mynet']
                },
                'server_node': {
                    'image': 'python:3.8-alpine',
                    'depends_on': ['network_switch'],
                    'networks': ['mynet']
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
                'command': 'sh - c "pip3 install -r requirements.txt && python client.py',
                'networks': ['mynet'],
                'volumes': ['./client.py:/client.py', './requirements.txt:/requirements.txt']
            }

            # Write the generated YAML data to a file
            with open('docker-compose.yml', 'w') as yaml_file:
                yaml.dump(docker_compose_data, yaml_file, default_flow_style=False)

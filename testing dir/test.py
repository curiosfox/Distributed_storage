from docker_deploy import DockerDeployment
if __name__ == "__main__":
    docker_deploy = DockerDeployment()
    docker_deploy.generate_yml_file(nodes=4)
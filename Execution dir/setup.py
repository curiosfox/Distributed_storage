import os
import subprocess
import shutil


class Setup(object):

    def initialize_clients(self, nodes=4):
        def copy_script(script_path, target_directory):
            target_path = os.path.join(target_directory, os.path.basename(script_path))
            shutil.copy(script_path, target_path)
            return target_path

        # Function to execute a Python script in a directory
        def execute_script(script_path, directory):
            os.chdir(directory)
            command = f"python3 {script_path}"
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(process)

        # List of directories where the scripts will be placed
        directories = list()
        for index in range(0, nodes):
            directory = f"directory_{index}"
            os.mkdir(directory)
            directories.append(directory)

        # Path to the Python script you want to distribute
        script_to_distribute = 'client.py'
        port_file = 'port.txt'
        # Copy the script to each directory and execute it
        for index, directory in enumerate(directories):
            with open(port_file, 'w') as f: f.write(str(5555 + index))
            copy_script(script_to_distribute, directory)
            copy_script(port_file, directory)
            execute_script(script_to_distribute, directory)
        # cleanup
        for directory in directories:
            shutil.rmtree(directory)

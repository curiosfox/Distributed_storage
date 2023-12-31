import os
import random
import shutil
import string


class FileOps:
    def __init__(self, file_size):
        self.file_size = file_size
        self.file_content = self.generate_file_content()

    def generate_file_content(self):
        return ''.join(random.choice(string.ascii_letters) for _ in range(self.file_size))

    def write_file(self, file_path, content):
        with open(file_path, 'w') as file:
            file.write(content)

    def read_file(self, file_path):
        with open(file_path, 'r') as file:
            return file.read()

    def generate_file(self, file_path):
        content = self.generate_file_content()
        self.write_file(file_path, content)
        return content

    def fragment_file(self, content, num_fragments):
        fragment_size = len(content) // num_fragments
        fragments = [content[i:i + fragment_size] for i in range(0, len(content), fragment_size)]
        return fragments

    def combine_fragments(self, fragments):
        return ''.join(fragments)

    def compare_files(self, original_content, combined_content):
        return original_content == combined_content

    def generate_and_fragment_file(self, file_path, num_fragments):
        content = self.generate_file(file_path)
        return self.fragment_file(content, num_fragments)

    @staticmethod
    def generate_files(directory_path, file_size_bytes):
        # Create the directory if it doesn't exist
        os.makedirs(directory_path, exist_ok=True)

        # Generate and write 100 files
        file_names = []
        for i in range(1, 101):
            file_name = f"file_{i}.txt"
            file_path = os.path.join(directory_path, file_name)
            file_content = ''.join(random.choices(string.ascii_letters + string.digits, k=file_size_bytes))

            with open(file_path, 'w') as file:
                file.write(file_content)

            file_names.append(file_path)

        return file_names

    @staticmethod
    def remove_directory(directory_path):
        try:
            shutil.rmtree(directory_path)
            print(f"Directory '{directory_path}' and its contents removed successfully.")
            return True
        except Exception as e:
            print(f"Error removing directory '{directory_path}': {e}")
            return False

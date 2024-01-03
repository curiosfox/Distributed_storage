import os
import random
import string


class FileOps:
    def __init__(self, file_size):
        self.file_size = file_size
        self.file_content = ""

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

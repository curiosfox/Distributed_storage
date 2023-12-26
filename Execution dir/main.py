import subprocess
import requests


class Main_process(object):

    def __init__(self):
        self.url = "http://127.0.0.1:1111/task1"

    def start_task1(self):
        response = requests.get(self.url)


if __name__ == "__main__":
    main_pro = Main_process()
    main_pro.start_task1()

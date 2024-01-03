import ast

import requests


class Result(object):
    def __init__(self):
        self.request = requests
        self.url = "http://127.0.0.1:5000"

    def task1_automation(self):
        final_result = dict()
        counter = 0

        for nodes in [3, 6, 12, 24]:
            for operation in ["random", "buddy", "min_copy"]:
                for file_size in [100 * 1024, 1000 * 1024, 10 * 1000 * 1024, 100 * 1000 * 1024]:
                    params_json = {
                        "nodes": nodes,
                        "operation": operation,
                        "file_size": file_size
                    }
                    print("params_json", params_json)

                    counter += 1
                    print(f"Processing count: {counter}")

                    final_result[f"Nodes:{nodes},  Operation:{operation},  filesize:{file_size}"] = ast.literal_eval(
                        self.request.post(f"{self.url}/task1", json=params_json).text)
        with open("final_result.json", "w") as file:
            file.write(final_result.__str__())


if __name__ == "__main__":
    result_obj = Result()
    result_obj.task1_automation()

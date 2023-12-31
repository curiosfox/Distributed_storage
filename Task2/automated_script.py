import ast

import requests


class Result(object):
    def __init__(self):
        self.request = requests
        self.url = "http://127.0.0.1:5000"

    def task2_automation(self):
        final_result = dict()
        for nodes in [12, 24, 36]:
            for operation in ["random", "buddy", "min_copy"]:
                params_json = {
                    "nodes": nodes,
                    "operation": operation
                }
                final_result[f"Nodes:{nodes}_Operation:{operation}"] = ast.literal_eval(
                    self.request.post(f"{self.url}/task2", json=params_json).text)
        with open("final_result.json", "w") as file:
            file.write(final_result.__str__())


if __name__ == "__main__":
    result_obj = Result()
    result_obj.task2_automation()

import json


def post(data):
    print(json.dumps(data, indent=4, sort_keys=True))
    input()
    return True

import json
import os
import spiders

data_file = "houses.json"

def save_houses(houses):
    marshalled = json.dumps(houses, indent=4, ensure_ascii=False)
    file = open(data_file, "w")
    file.write(marshalled.encode("utf-8"))

def load_houses():
    if not os.path.isfile(data_file):
        return []
    marshalled = open(data_file).read()
    return json.loads(marshalled)

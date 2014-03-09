import json
import spiders

def save_houses(houses):
    marshalled = json.dumps(houses, indent=4, ensure_ascii=False)
    file = open("houses.json", "w")
    file.write(marshalled.encode("utf-8"))

def load_houses():
    marshalled = open("houses.json").read()
    return json.loads(marshalled)

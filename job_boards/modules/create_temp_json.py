import json
from os.path import isfile

data = []

def createJSON(item):
    if isfile("./data/temp/temp_data.json"):
        print("Deleting temp_data.json content")
        t = open(f"./data/temp/temp_data.json", "r+")
        t.truncate(0)
        t.close()

    with open("./data/temp/temp_data.json", "a", encoding="utf-8") as file:
        print("Generating new temp_data.json")
        json.dump(data, file, ensure_ascii=False, indent=4)

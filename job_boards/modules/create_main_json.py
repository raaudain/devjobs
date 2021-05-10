import json
from os.path import isfile


def createJSON():
        f = open(f"./data/temp/temp_data.json")
        data = json.load(f)
        f.close()

        if isfile("./data/data.json"):
                print("=> Deleting old data.json content")
                t = open(f"./data/data.json", "r+")
                t.truncate(0)
                t.close()

        orderedData = sorted(data, key=lambda i: i["timestamp"], reverse=True)

        with open("./data/data.json", "a", encoding="utf-8") as file:
                print("=> Generating new data.json content")
                json.dump(orderedData, file, ensure_ascii=False, indent=4)

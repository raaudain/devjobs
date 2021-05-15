import json
from os.path import isfile

data = []

def createJSON():
    if isfile("./server/data/temp/temp_data.json"):
        print("=> temp_data.json: Deleting old content")
        t = open(f"./server/data/temp/temp_data.json", "r+")
        t.truncate(0)
        t.close()

    with open("./server/data/temp/temp_data.json", "a", encoding="utf-8") as file:
        print("=> temp_data.json: Generating new content")
        json.dump(data, file, ensure_ascii=False, indent=4)

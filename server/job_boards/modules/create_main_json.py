import json
import sys
from os.path import isfile


def createJSON():
    temp = "./data/temp/temp_data.json"
    f = open(temp)
    data = json.load(f)
    f.close()
    main = "./data/data.json"
    if isfile(main):
        print("=> data.json: Deleting old content")
        t = open(main, "r+")
        t.truncate(0)
        t.close()
    orderedData = sorted(data, key=lambda i: i["timestamp"], reverse=True)
    with open(main, "a", encoding="utf-8") as file:
        print("=> data.json: Generating new content")
        json.dump(orderedData, file, ensure_ascii=False, indent=4)

# createJSON()

# sys.exit(0)

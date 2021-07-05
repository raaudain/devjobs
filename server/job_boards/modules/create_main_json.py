import json, sys
from os.path import isfile


def createJSON():


        # f = open(f"./data/temp/temp_data.json")
        # data = json.load(f)
        # f.close()

        temp = "./data/temp/temp_data.json"

        f = open(temp)
        data = json.load(f)
        f.close()

        # if isfile("./data/data.json"):
        #         print("=> data.json: Deleting old content")
        #         t = open(f"./data/data.json", "r+")
        #         t.truncate(0)
        #         t.close()
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

createJSON()

sys.exit(0)
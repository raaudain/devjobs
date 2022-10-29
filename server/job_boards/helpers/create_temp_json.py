import json
import sys
from os.path import isfile


data = []
scraped = set()


def createJSON(item):
    temp = "./data/temp/temp_data.json"
    if isfile(temp):
        print("=> temp_data.json: Deleting old content")
        t = open(temp, "r+")
        t.truncate(0)
        t.close()
    with open(temp, "a", encoding="utf-8") as file:
        print("=> temp_data.json: Generating new content")
        json.dump(data, file, ensure_ascii=False, indent=4)


# createJSON("./data/temp/temp_data.json")
# sys.exit(0)

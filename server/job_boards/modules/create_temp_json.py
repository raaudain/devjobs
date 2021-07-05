import json, sys
from os.path import isfile
# from server.job_boards.modules import create_main_json

data = []
scraped = set()

def createJSON(item):
    # global data
    # temp = "../../data/temp/temp_data.json"
    temp = "./data/temp/temp_data.json"
    
    # if isfile("./data/temp/temp_data.json"):
    #     print("=> temp_data.json: Deleting old content")
    #     t = open(f"./data/temp/temp_data.json", "r+")
    #     t.truncate(0)
    #     t.close()


    if isfile(temp):
        print("=> temp_data.json: Deleting old content")
        t = open(temp, "r+")
        t.truncate(0)
        t.close()

    with open(temp, "a", encoding="utf-8") as file:
        print("=> temp_data.json: Generating new content")
        json.dump(data, file, ensure_ascii=False, indent=4)

    # data = []
    # scraped.clear()

createJSON(data)


# createJSON("./data/temp/temp_data.json")
# sys.exit(0)
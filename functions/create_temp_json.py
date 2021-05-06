import json

class tempJSON:
    data = ["Test"]

    def createJSON(item):
        with open("./data/temp/temp_data.json", "a", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
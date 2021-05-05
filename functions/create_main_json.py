import json

f = open(f"./data/temp/temp_data.json")
data = json.load(f)
f.close()

orderedData = sorted(data, key=lambda i: i["timestamp"], reverse=True)

with open("./data/data.json", "a", encoding="utf-8") as file:
        json.dump(orderedData, file, ensure_ascii=False, indent=4)


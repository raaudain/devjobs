import json

f = open(f"./data/data.json")
data = json.load(f)
f.close()

ordered = sorted(data, key=lambda i: i["timestamp"], reverse=True)

with open("./data/data.json", "a", encoding="utf-8") as file:
        json.dump(ordered, file, ensure_ascii=False, indent=4)
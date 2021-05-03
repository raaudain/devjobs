from datetime import datetime
import json
import operator

f = open(f"./data/data.json")
data = json.load(f)
# f.close()

# print(data)

for i in data:
    print(i)
    

# print sorted(lis, key = lambda i: i['age'])
# datetime.timestamp(datetime.strptime(date, "%Y-%m-%d %H:%M"))
# print(sorted(data, key=lambda i: i["timestamp"]))
import json

f = open("save.json")

data = json.load(f)

print(data["data"]["PlayerList"][0])
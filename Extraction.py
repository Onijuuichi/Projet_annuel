import json
test = open('test.json', "r")
data = json.loads(test.read())


for i in data:
    print(i['NombreFractionsDelivrees'])
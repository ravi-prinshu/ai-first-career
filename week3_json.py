import json

# person = {
#     "name": "Ravi",
#     "age": 30,
#     "role": "Business Analyst"
# }

# json_data = json.dumps(person)

# print(json_data)

json_data = '{"name": "Ravi", "age": 30, "role": "Business Analyst"}'

person = json.loads(json_data)

print(person["name"])
print(person["age"])
print(person["role"])
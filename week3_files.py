# with open("profile.txt", "w") as file:
#     file.write("Ravi")

with open("profile.txt", "a") as file:
    file.write("\nBusiness Analyst")

with open("profile.txt", "r") as file:
    content = file.read()

print(content)
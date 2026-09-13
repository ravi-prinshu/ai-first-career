

import requests

response = requests.get("https://api.github.com")

data = response.json()

if response.status_code== 200:
    print ("API request successful")
    print(data["current_user_url"])
else:
    print("API failed")

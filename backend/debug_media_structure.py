import requests
import json
import os

API_KEY = "1be1c7ba0cmshe32f21eae5a8e45p14cc17jsnb61808273166"
HOST = "instagram-best-experience.p.rapidapi.com"
USER_ID = "13460080" # Nike

url = f"https://{HOST}/feed"
params = {"user_id": USER_ID}
headers = {
	"x-rapidapi-key": API_KEY,
	"x-rapidapi-host": HOST
}

print(f"Testing Feed Structure for {USER_ID}")

try:
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        print("SUCCESS")
        if isinstance(data, dict):
            print("Root Keys:", list(data.keys()))
            # Inspect first item if 'items' or 'data' exists
            if "items" in data:
                print("Items found:", len(data["items"]))
                if len(data["items"]) > 0:
                    print("First Item Keys:", list(data["items"][0].keys()))
            elif "data" in data:
                 print("Data Keys:", list(data["data"].keys()))
        else:
            print("Response is a list, len:", len(data))
            if len(data) > 0:
                print("First Item Keys:", list(data[0].keys()))
                
        print("Snippet:", json.dumps(data, indent=2)[:500])
    else:
        print("Error:", response.status_code, response.text)
except Exception as e:
    print(e)

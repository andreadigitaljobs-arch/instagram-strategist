import requests
import os
import json

API_KEY = "1be1c7ba0cmshe32f21eae5a8e45p14cc17jsnb61808273166"
HOST = "instagram-best-experience.p.rapidapi.com"
USER_ID = "13460080" # Nike

headers = {
	"x-rapidapi-key": API_KEY,
	"x-rapidapi-host": HOST
}

endpoints = [
    "/feed",
    "/user/feed",
    "/media",
    "/user/media",
    "/posts",
    "/user/posts"
]

print(f"Testing Media Endpoints for User ID: {USER_ID}")

for ep in endpoints:
    url = f"https://{HOST}{ep}"
    print(f"\n--- Testing: {ep} ---")
    
    # Try with user_id param
    params = {"user_id": USER_ID}
    try:
        response = requests.get(url, headers=headers, params=params)
        print(f"Status ({ep}): {response.status_code}")
        if response.status_code == 200:
             print("✅ SUCCESS!")
             print(response.text[:300])
             break
        elif response.status_code == 400:
             # Might need 'id' instead of 'user_id'
             response = requests.get(url, headers=headers, params={"id": USER_ID})
             print(f"Status ({ep} w/ id): {response.status_code}")
             if response.status_code == 200:
                 print("✅ SUCCESS!")
                 print(response.text[:300])
                 break
    except Exception as e:
        print(e)

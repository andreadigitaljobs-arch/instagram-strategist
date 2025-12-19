import requests
import os
import json

API_KEY = "1be1c7ba0cmshe32f21eae5a8e45p14cc17jsnb61808273166"
HOST = "instagram-best-experience.p.rapidapi.com"

# Nike ID found previously: 13460080
user_id = "13460080" # Nike

endpoints = [
    f"/user/{user_id}/feed",
    f"/user/{user_id}/media",
    f"/users/{user_id}/media",
    f"/users/{user_id}/posts",
    "/user/posts", # Might take param
    f"/v1/users/{user_id}/media_recent"
]

for ep in endpoints:
    url = f"https://{HOST}{ep}"
    print(f"\n--- Testing Endpoint: {ep} ---")
    
    # Try with and without params
    try:
        response = requests.get(url, headers=headers)
        print(f"Status (Direct): {response.status_code}")
        if response.status_code == 200:
             print("✅ SUCCESS!")
             print(response.text[:200])
             break
             
        # Try with user_id param if url didn't have it
        if "{user_id}" not in ep:
             response = requests.get(url, headers=headers, params={"user_id": user_id})
             print(f"Status (Param): {response.status_code}")
             if response.status_code == 200:
                 print("✅ SUCCESS!")
                 break
    except Exception as e:
        print(e)

except Exception as e:
    print(f"Exception: {e}")

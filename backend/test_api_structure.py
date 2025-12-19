import requests
import os
import json

# Manual load .env
env = {}
try:
    with open(".env", "r") as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                key, val = line.strip().split("=", 1)
                os.environ[key] = val
except:
    pass

API_KEY = os.environ.get("RAPIDAPI_KEY")
HOST = os.environ.get("RAPIDAPI_HOST")

headers = {
	"x-rapidapi-key": API_KEY,
	"x-rapidapi-host": HOST
}

print(f"Testing Host: {HOST}")

endpoints = [
    "/profile", 
    "/users/profile",
    "/v1/users/profile",
    "/ig/profile"
]

for ep in endpoints:
    url = f"https://{HOST}{ep}"
    print(f"\n--- Testing Endpoint: {ep} ---")
    
    param_sets = [
        {"username": "nike"},
        {"user": "nike"},
        {"username_or_id_or_url": "nike"},
        {"id": "nike"},
        {"short_code": "nike"}
    ]
    
    for params in param_sets:
        try:
            response = requests.get(url, headers=headers, params=params)
            
            print(f"Status ({list(params.keys())[0]}): {response.status_code}")
            
            if response.status_code == 200:
                print(f"✅ SUCCESS! Endpoint: {ep} | Params: {params}")
                print("Response Snippet:", response.text[:200])
                break
            elif response.status_code == 400 or response.status_code == 422:
                print(f"⚠️  Client Error ({response.status_code}) Body: {response.text}")
                
        except Exception as e:
            pass
        try:
            response = requests.get(url, headers=headers, params=params)
             # If it's a proxy, it might require a trailing slash or not
            if response.status_code == 404:
                 # Try adding slash
                 if not url.endswith("/"):
                    response = requests.get(url + "/", headers=headers, params=params)
            
            if response.status_code == 200:
                print(f"✅ SUCCESS! Endpoint: {ep} | Params: {list(params.keys())[0]}")
                print("Response Snippet:", response.text[:200])
                break
            else:
                print(f"Status ({list(params.keys())[0]}): {response.status_code}")
        except Exception as e:
            pass

headers = {
	"x-rapidapi-key": API_KEY,
	"x-rapidapi-host": HOST
}

try:
    response = requests.get(url, headers=headers, params=querystring)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("Root Keys:", list(data.keys()))
        if "data" in data:
            print("Data Keys:", list(data["data"].keys()))
        if "user" in data:
            print("User Keys:", list(data["user"].keys()))
        
        # Dump a small part to see structure
        print("Snippet:", json.dumps(data, indent=2)[:500])
    else:
        print("Error Response:", response.text)

except Exception as e:
    print(f"Exception: {e}")

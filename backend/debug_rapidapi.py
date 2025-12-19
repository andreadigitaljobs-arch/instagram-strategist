import requests
import os

# Manual load for testing
try:
    with open(".env", "r") as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                key, val = line.strip().split("=", 1)
                os.environ[key] = val
except Exception:
    print("Could not load .env file")

API_KEY = os.environ.get("RAPIDAPI_KEY")
HOST = os.environ.get("RAPIDAPI_HOST")

print(f"Testing with Host: {HOST}")
print(f"Key present: {bool(API_KEY)}")

url = f"https://{HOST}/ig/info_username/"
querystring = {"user": "nike"} # Test with a known username

headers = {
	"x-rapidapi-key": API_KEY,
	"x-rapidapi-host": HOST
}

try:
    print(f"Requesting: {url}")
    response = requests.get(url, headers=headers, params=querystring)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text[:500]}...") # Print first 500 chars
except Exception as e:
    print(f"Error: {e}")

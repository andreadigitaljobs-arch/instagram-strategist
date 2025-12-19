import instaloader
import sys

def test_scrape(handle):
    print(f"Attempting to scrape {handle}...")
    L = instaloader.Instaloader()
    try:
        profile = instaloader.Profile.from_username(L.context, handle)
        print(f"Success! Found profile: {profile.username}")
        print(f"Followers: {profile.followers}")
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")

if __name__ == "__main__":
    test_scrape("nike")

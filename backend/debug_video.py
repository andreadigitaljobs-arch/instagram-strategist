import yt_dlp
import instaloader
import sys

url = "https://www.instagram.com/reel/DSNT25LDafy/"

print(f"Testing download for: {url}")

print("\n--- TEST 1: yt-dlp ---")
try:
    ydl_opts = {
        'format': 'best',
        'quiet': False,
        'no_warnings': False,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False) # Just extract info first
        print("yt-dlp Success!")
        print(f"Title: {info.get('title')}")
        print(f"URL: {info.get('url')}")
except Exception as e:
    print(f"yt-dlp Failed: {e}")

print("\n--- TEST 2: Instaloader ---")
try:
    L = instaloader.Instaloader()
    shortcode = url.split("/reel/")[1].split("/")[0]
    print(f"Shortcode: {shortcode}")
    post = instaloader.Post.from_shortcode(L.context, shortcode)
    print("Instaloader Success!")
    print(f"Video URL: {post.video_url}")
except Exception as e:
    print(f"Instaloader Failed: {e}")

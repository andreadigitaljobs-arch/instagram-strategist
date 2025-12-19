import requests
import os
from models import Profile, Post, ProfileStats, PostType, ContentCategory

# RAPIDAPI CONFIG
# We default to "Instagram Best Experience" by Lobster
RAPIDAPI_KEY = "YOUR_RAPIDAPI_KEY_HERE" 
RAPIDAPI_HOST = "instagram-best-experience.p.rapidapi.com" 

def scrape_profile(handle: str) -> Profile:
    """
    Scrapes using RapidAPI to avoid IP Bans.
    """
    username = handle.lstrip('@')
    # This specific API (Best Experience) uses /profile
    url = f"https://{RAPIDAPI_HOST}/profile"
    
    querystring = {"username": username}
    
    headers = {
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY", RAPIDAPI_KEY),
        "X-RapidAPI-Host": os.getenv("RAPIDAPI_HOST", RAPIDAPI_HOST)
    }
    
    # 1. CALL API
    response = requests.get(url, headers=headers, params=querystring)
    
    # 2. CHECK LIMITS
    remaining = response.headers.get("x-ratelimit-requests-remaining", "Unknown")
    print(f"API Credits Remaining: {remaining}")
    
    if response.status_code == 429:
        raise ValueError("⚠️ Has alcanzado el límite gratuito de la API. (0 créditos restantes)")
        
    if response.status_code != 200:
        raise ValueError(f"Error API ({response.status_code}): {response.text}")

    data = response.json()
    
    # Mapping for "Instagram Best Experience" (Flat Structure)
    # Keys found: pk, username, full_name, follower_count, media_count, following_count, biography, profile_pic_url
    
    if "pk" not in data:
         raise ValueError("Usuario no encontrado o privado (API no devolvió ID).")


    
    # 3. GET CONTENT (FEED)
    # Now that we have the PK, we can fetch the media
    user_id = data["pk"]
    posts = []
    
    print(f"DEBUG: Fetching feed for User ID: {user_id}")
    
    try:
        feed_url = f"https://{RAPIDAPI_HOST}/feed"
        # params={"user_id": user_id} was confirmed in tests
        feed_response = requests.get(feed_url, headers=headers, params={"user_id": user_id})
        
        print(f"DEBUG: Feed Status: {feed_response.status_code}")
        
        if feed_response.status_code == 200:
            feed_data = feed_response.json()
            items = feed_data.get("items", [])
            print(f"DEBUG: Items found: {len(items)}")
            
            for item in items[:6]: # Get top 6
                try:
                    # Image URL
                    image_url = ""
                    if "image_versions2" in item and "candidates" in item["image_versions2"]:
                        candidates = item["image_versions2"]["candidates"]
                        if candidates:
                            image_url = candidates[0].get("url", "")
                    
                    # Caption
                    caption = ""
                    if item.get("caption") and isinstance(item["caption"], dict):
                        caption = item["caption"].get("text", "")
                        
                    param_type = "static"
                    mt = item.get("media_type")
                    if mt == 1:
                        param_type = "static"
                    elif mt == 2:
                        param_type = "reel"
                    elif mt == 8:
                        param_type = "carousel"
                        
                    post = Post(
                        id=str(item.get("pk", "")),
                        caption=caption,
                        likes=item.get("like_count", 0),
                        comments=item.get("comment_count", 0),
                        image_url=image_url,
                        type=param_type, 
                        timestamp=str(item.get("taken_at", ""))
                    )
                    posts.append(post)
                except Exception as post_e:
                    print(f"DEBUG: Error parsing item: {post_e}")
                    pass
                    
    except Exception as e:
        print(f"Error fetching feed: {e}")
        # Continue without posts if feed fails
        pass

    # 4. CALCULATE METRICS
    engagement_rate = 0.0
    posts_per_week = 0.0
    
    if posts and data.get("follower_count", 0) > 0:
        total_interactions = sum(p.likes + p.comments for p in posts)
        avg_interactions = total_interactions / len(posts)
        engagement_rate = round((avg_interactions / data["follower_count"]) * 100, 2)
        print(f"DEBUG: Calculated ER: {engagement_rate}% (Avg: {avg_interactions}, Followers: {data['follower_count']})")
        
        # Simple posts per week estimation if we have at least 2 posts with timestamps
        try:
            if len(posts) >= 2:
                # Timestamps are strings, convert to int
                t_new = int(posts[0].timestamp)
                t_old = int(posts[-1].timestamp)
                diff_days = (t_new - t_old) / (24 * 3600)
                if diff_days > 0:
                    posts_per_week = round((len(posts) / diff_days) * 7, 1)
                    print(f"DEBUG: Calculated Freq: {posts_per_week} posts/week")
        except Exception as e:
            print(f"DEBUG: Error calculating frequency: {e}")

    stats = ProfileStats(
        total_posts=data.get("media_count", 0),
        followers=data.get("follower_count", 0),
        following=data.get("following_count", 0),
        engagement_rate=engagement_rate,
        posts_per_week=posts_per_week
    )

    return Profile(
        handle=f"@{data.get('username', username)}",
        name=data.get("full_name", ""),
        bio=data.get("biography", ""),
        profile_pic_url=data.get("profile_pic_url", ""),
        stats=stats,
        posts=posts,
        api_credits=remaining
    )

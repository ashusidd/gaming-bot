import requests
import os

PAGE_ID = '318640404662743'
ACCESS_TOKEN = os.environ.get('FB_TOKEN')

def post_to_facebook():
    # URL ko dhyan se dekho, niche slash (/) lagana bahut zaruri hai
    url = f"https://facebook.com{PAGE_ID}/feed"
    
    message = "🎮 Daily Gaming Update: New levels and epic moments! 🔥 #Gaming #ErAshuGaming"
    
    payload = {
        'message': message,
        'access_token': ACCESS_TOKEN
    }
    
    try:
        response = requests.post(url, data=payload)
        print(f"Server Response: {response.json()}")
    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    post_to_facebook()

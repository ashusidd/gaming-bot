import requests
import os

# Your Details
PAGE_ID = '318640404662743'
ACCESS_TOKEN = os.environ.get('FB_TOKEN')

def post_to_facebook():
    # Fixed URL with proper slash
    url = "https://facebook.com" + PAGE_ID + "/feed"
    
    message = "🎮 Daily Gaming Update: Stay tuned for epic highlights! 🔥 #Gaming #ErAshuGaming"
    
    payload = {
        'message': message,
        'access_token': ACCESS_TOKEN
    }
    
    try:
        response = requests.post(url, data=payload)
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    post_to_facebook()

import requests
import os

PAGE_ID = '318640404662743'
ACCESS_TOKEN = os.environ.get('FB_TOKEN')

def post_to_facebook():
    # URL ekdum perfect hai
    url = f"https://facebook.com{PAGE_ID}/feed"
    message = "🎮 Daily Gaming Update: Stay tuned for epic highlights! 🔥 #Gaming #ErAshuGaming"
    payload = {'message': message, 'access_token': ACCESS_TOKEN}
    
    r = requests.post(url, data=payload)
    print(r.json())

if __name__ == "__main__":
    post_to_facebook()

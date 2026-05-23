import requests
import os

PAGE_ID = '318640404662743'
ACCESS_TOKEN = os.environ.get('FB_TOKEN')

def post_to_facebook():
    message = "🎮 Daily Gaming Update: New levels and epic moments! 🔥 #Gaming #ErAshuGaming"
    url = f"https://facebook.com{PAGE_ID}/feed"
    payload = {'message': message, 'access_token': ACCESS_TOKEN}
    
    response = requests.post(url, data=payload)
    print(response.json())

if __name__ == "__main__":
    post_to_facebook()

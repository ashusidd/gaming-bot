import requests
import os

# Details
PAGE_ID = '318640404662743'
ACCESS_TOKEN = os.environ.get('FB_TOKEN')

def post_to_facebook():
    # Is URL ko dhyan se dekho, isme maine koi variable use nahi kiya taaki galti na ho
    url = "https://facebook.com"
    
    message = "🎮 Daily Gaming Update: Stay tuned for epic highlights! 🔥 #Gaming #ErAshuGaming"
    
    payload = {
        'message': message,
        'access_token': ACCESS_TOKEN
    }
    
    r = requests.post(url, data=payload)
    print(r.json())

if __name__ == "__main__":
    post_to_facebook()

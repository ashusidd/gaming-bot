import requests
import os

PAGE_ID = '318640404662743'
ACCESS_TOKEN = os.environ.get('FB_TOKEN')

def post_to_facebook():
    url = f"https://facebook.com{PAGE_ID}/feed"
    message = "🎮 Testing Autopilot Mode! 🔥 #Gaming #ErAshuGaming"
    payload = {'message': message, 'access_token': ACCESS_TOKEN}
    
    response = requests.post(url, data=payload)
    
    # Isse humein asli wajah pata chalegi
    print(f"Status Code: {response.status_code}")
    print(f"Full Response: {response.text}")

if __name__ == "__main__":
    post_to_facebook()

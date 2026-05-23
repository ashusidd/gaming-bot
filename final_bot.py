import requests
import os

PAGE_ID = '318640404662743'
FB_TOKEN = os.environ.get('FB_TOKEN')

def post_to_facebook():
    # Is URL ko dhyan se dekho, isme galti ki gunjayish nahi hai
    url = f"https://facebook.com{PAGE_ID}/feed"
    
    payload = {
        'message': "🎮 Gaming Mode ON! 🔥 #Gaming #ErAshuGaming",
        'access_token': FB_TOKEN
    }
    
    response = requests.post(url, data=payload)
    print(response.json())

if __name__ == "__main__":
    post_to_facebook()

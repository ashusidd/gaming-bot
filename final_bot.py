import requests
import os

def post_to_facebook():
    # IS LINE KO DHAYAN SE DEKHO - ISME SLASH (/) HAI
    url = "https://facebook.com"
    
    token = os.environ.get('FB_TOKEN')
    
    data = {
        'message': '🎮 Gaming Mode ON! 🔥 #Gaming #ErAshuGaming',
        'access_token': token
    }
    
    r = requests.post(url, data=data)
    print(r.json())

if __name__ == "__main__":
    post_to_facebook()

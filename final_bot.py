import requests
import os

def post_to_facebook():
    url = "https://facebook.com"
    token = os.environ.get('FB_TOKEN')
    
    if not token:
        print("❌ Token nahi mila! Settings check karein.")
        return

    data = {
        'message': '🎮 Testing Autopilot! 🔥 #Gaming #ErAshuGaming',
        'access_token': token
    }
    
    response = requests.post(url, data=data)
    
    # Isse humein asli wajah pata chalegi
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    post_to_facebook()

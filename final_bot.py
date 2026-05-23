import requests
import os
from google import genai

def get_ai_content():
    try:
        api_key = os.environ.get('GEMINI_API_KEY')
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents="Write a short viral gaming news post (FREEFIRE, GTA 6, BGMI) for a Facebook page with emojis and hashtags."
        )
        return response.text
    except Exception as e:
        return "🎮 Gaming Mode ON! 🔥 Stay tuned for epic updates! #Gaming #ErAshuGaming"

def post_to_facebook():
    # Maine URL ko ekdum saaf-saaf likh diya hai bina kisi bracket ke
    url = "https://facebook.com"
    
    token = os.environ.get('FB_TOKEN')
    message = get_ai_content()
    
    payload = {
        'message': message, 
        'access_token': token
    }
    
    try:
        r = requests.post(url, data=payload)
        print("Facebook Response:", r.json())
    except Exception as e:
        print("Facebook Post Error:", e)

if __name__ == "__main__":
    post_to_facebook()

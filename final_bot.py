import requests
import os
from google import genai

def get_ai_content():
    try:
        api_key = os.environ.get('GEMINI_API_KEY')
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents="Write a short viral gaming news post (freefire, bgmi, gta6) for Facebook with emojis and hashtags in hinglish."
        )
        return response.text
    except Exception as e:
        return "🎮 Gaming Mode ON! 🔥 Stay tuned for epic updates. #Gaming #ErAshuGaming"

def post_to_facebook():
    url = "https://facebook.com"
    token = os.environ.get('FB_TOKEN')
    message = get_ai_content()
    
    payload = {'message': message, 'access_token': token}
    r = requests.post(url, data=payload)
    print("Facebook Response:", r.text)

if __name__ == "__main__":
    post_to_facebook()

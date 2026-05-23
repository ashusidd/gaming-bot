import requests
import os
from google import genai

def get_ai_content():
    try:
        api_key = os.environ.get('GEMINI_API_KEY')
        client = genai.Client(api_key=api_key)
        
        # AI ko Hinglish aur Gaming topics ke liye instruction
        prompt = (
            "Write a viral Hinglish (Hindi + English) gaming post for Facebook. "
            "The topic should be about Free Fire, BGMI, or GTA 6 news/memes. "
            "Keep it funny, engaging, use lots of emojis and trending hashtags. "
            "Target audience: Indian gamers."
        )
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"AI Error: {e}")
        return "Bhaiyo, naya gaming update aane wala hai! Taiyaar ho jao. 🎮🔥 #Gaming #BGMI #FreeFire #GTA6"

def post_to_facebook():
    page_id = '318640404662743'
    # API URL jiske zariye post hogi
    url = f"https://facebook.com{page_id}/feed"
    
    token = os.environ.get('FB_TOKEN')
    message = get_ai_content()
    
    payload = {'message': message, 'access_token': token}
    
    r = requests.post(url, data=payload)
    print(f"Facebook Response: {r.json()}")

if __name__ == "__main__":
    post_to_facebook()

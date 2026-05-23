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
            model="gemini-1.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"AI Error: {e}")
        return "Bhaiyo, naya gaming update aane wala hai! Taiyaar ho jao. 🎮🔥 #Gaming #BGMI #FreeFire #GTA6"

def post_to_facebook():
    page_id = '318640404662743'
    system_token = os.environ.get('FB_TOKEN')
    
    # ---------------------------------------------------------
    # NEW MAGIC STEP: System Token ko Page Token mein convert karna
    # ---------------------------------------------------------
    token_url = f"https://graph.facebook.com/{page_id}?fields=access_token&access_token={system_token}"
    token_response = requests.get(token_url).json()
    
    if 'access_token' in token_response:
        page_token = token_response['access_token']
        print("Success: Page Access Token mil gaya!")
    else:
        print(f"Token Error: {token_response}")
        return
    # ---------------------------------------------------------
    
    # API URL jiske zariye post hogi
    url = f"https://graph.facebook.com/{page_id}/feed"
    message = get_ai_content()
    
    # Ab hum yahan naya 'page_token' bhej rahe hain
    payload = {'message': message, 'access_token': page_token}
    
    r = requests.post(url, data=payload)
    print(f"Facebook Response: {r.json()}")

if __name__ == "__main__":
    post_to_facebook()

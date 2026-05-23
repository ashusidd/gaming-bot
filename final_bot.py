import requests
import os
from google import genai

def get_ai_content():
    try:
        api_key = os.environ.get('GEMINI_API_KEY')
        client = genai.Client(api_key=api_key)
        
        # Latest Gemini Model
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents="Write a short viral gaming news post (FREEFIRE, GTA 6, BGMI, or Gaming Tech) for a Facebook page with emojis and hashtags."
        )
        return response.text
    except Exception as e:
        # Agar AI busy ho ya limit khatam ho, toh ye backup message jayega
        print(f"AI Error: {e}")
        return "🎮 Gaming Mode ON! 🔥 Stay tuned for epic updates and viral highlights coming your way! #Gaming #ErAshuGaming #ViralNews"

def post_to_facebook():
    # --- YAHAN SLASH (/) KA DHAYAN RAKHEIN ---
    page_id = '318640404662743'
    url = f"https://facebook.com{page_id}/feed"
    
    token = os.environ.get('FB_TOKEN')
    message = get_ai_content()
    
    payload = {'message': message, 'access_token': token}
    
    try:
        r = requests.post(url, data=payload)
        print(r.json())
    except Exception as e:
        print(f"Facebook Post Error: {e}")

if __name__ == "__main__":
    post_to_facebook()

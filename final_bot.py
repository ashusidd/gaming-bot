import requests
import os
import google.generativeai as genai

def get_ai_content():
    try:
        # Gemini API setup
        genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = "Write a short, viral gaming news post about FREEFIRE, BGMI or GTA 6 in hinglish for Facebook."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return "🎮 Gaming Mode ON! 🔥 #Gaming #ErAshuGaming"

def post_to_facebook():
    # URL EKDUM FIXED HAI - KOI BRACKET NAHI HAI
    url = "https://facebook.com"
    
    token = os.environ.get('FB_TOKEN')
    message = get_ai_content()
    
    # Data ko alag se bhej rahe hain
    payload = {
        'message': message,
        'access_token': token
    }
    
    # Request bhej rahe hain
    r = requests.post(url, data=payload)
    print("Facebook Response:", r.json())

if __name__ == "__main__":
    post_to_facebook()

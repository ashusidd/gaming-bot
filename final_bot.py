import requests
import os
import google.generativeai as genai

def get_ai_content():
    # Gemini Setup
    api_key = os.environ.get('GEMINI_API_KEY')
    genai.configure(api_key=api_key)
    
    model = genai.GenerativeModel('gemini-1.5-flash') # Naya aur fast model
    
    prompt = "Write a very short, viral gaming news post (GTA 6 or BGMI) for a Facebook page with emojis and hashtags. Keep it engaging."
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"🎮 Gaming Mode ON! 🔥 Stay tuned for epic updates. #Gaming #Viral"

def post_to_facebook():
    page_id = '318640404662743'
    token = os.environ.get('FB_TOKEN')
    
    message = get_ai_content()
    
    url = f"https://facebook.com{page_id}/feed"
    payload = {'message': message, 'access_token': token}
    
    r = requests.post(url, data=payload)
    print(r.json())

if __name__ == "__main__":
    post_to_facebook()

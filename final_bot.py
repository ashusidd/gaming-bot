import requests
import os
import google.generativeai as genai

def get_ai_content():
    genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
    model = genai.GenerativeModel('gemini-pro')
    prompt = "Write a short, engaging gaming news post for a Facebook page (80k followers). Topic: Trending Games (GTA 6, BGMI, etc). Use emojis and hashtags."
    response = model.generate_content(prompt)
    return response.text

def post_to_facebook():
    message = get_ai_content()
    url = f"https://facebook.com"
    payload = {'message': message, 'access_token': os.environ.get('FB_TOKEN')}
    r = requests.post(url, data=payload)
    print(r.json())

if __name__ == "__main__":
    post_to_facebook()

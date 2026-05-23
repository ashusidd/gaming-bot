import requests
import os
from google import genai

def get_ai_content():
    api_key = os.environ.get('GEMINI_API_KEY')
    client = genai.Client(api_key=api_key)
    
    # Naya AI model use kar rahe hain
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Write a short viral gaming news post for Facebook with emojis and hashtags."
    )
    return response.text

def post_to_facebook():
    # URL ko dhyan se dekho, isme slash (/) fixed hai
    page_id = '318640404662743'
    url = f"https://facebook.com{page_id}/feed"
    
    token = os.environ.get('FB_TOKEN')
    message = get_ai_content()
    
    payload = {'message': message, 'access_token': token}
    
    r = requests.post(url, data=payload)
    print(r.json())

if __name__ == "__main__":
    post_to_facebook()

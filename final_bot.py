import requests
import os
import random
import time

def get_ai_content():
    try:
        # Ab hum Google ki jagah Groq ki chabi use kar rahe hain
        api_key = os.environ.get('GROQ_API_KEY') 
        
        topics = [
            "a funny meme story or relatable situation about BGMI campers",
            "latest news, leaks or exciting rumors about GTA 6",
            "pro tips and secret tricks for Free Fire players",
            "a relatable Indian gamer struggle (like high ping, game lagging, or mom scolding while gaming)",
            "a 'Reaction Poll' asking Indian gamers to choose between two popular games. Ask them to use Facebook reactions (Like 👍 for Game A, Heart ❤️ for Game B) to vote."
        ]
        chosen_topic = random.choice(topics)
        
        prompt = (
            f"Write a viral Hinglish (Hindi + English) gaming Facebook post about: {chosen_topic}. "
            "Keep it funny, highly engaging, use lots of emojis and trending hashtags. "
            "Target audience: Indian gamers."
        )
        
        # Groq API ka Darwaza (Endpoint)
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Llama 3 model Meta (Facebook) ka hi banaya hua open-source AI hai
        data = {
            "model": "llama3-8b-8192", 
            "messages": [{"role": "user", "content": prompt}]
        }
        
        print("Groq AI se naya content mang rahe hain...")
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        
        return result['choices'][0]['message']['content']
        
    except Exception as e:
        print(f"AI Error: {e}")
        return "Bhaiyo, naya gaming update aane wala hai! Taiyaar ho jao. 🎮🔥 #Gaming #BGMI #FreeFire #GTA6"

def post_to_facebook():
    page_id = '318640404662743' # Aapke Engineers Gamer page ka ID
    system_token = os.environ.get('FB_TOKEN')
    
    # System Token ko Page Token mein convert karna
    token_url = f"https://graph.facebook.com/{page_id}?fields=access_token&access_token={system_token}"
    token_response = requests.get(token_url).json()
    
    if 'access_token' in token_response:
        page_token = token_response['access_token']
        print("Success: Page Access Token mil gaya!")
    else:
        print(f"Token Error: {token_response}")
        return
    
    # Facebook par post upload karna
    url = f"https://graph.facebook.com/{page_id}/feed"
    message = get_ai_content()
    
    payload = {'message': message, 'access_token': page_token}
    
    r = requests.post(url, data=payload)
    print(f"Facebook Response: {r.json()}")

if __name__ == "__main__":
    post_to_facebook()

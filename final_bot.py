import requests
import os
import random

def get_ai_content():
    try:
        api_key = os.environ.get('GROQ_API_KEY')
        
        # DEBUG CHECK 1: Kya GitHub ne chabi bheji?
        if not api_key:
            print("❌ FATAL ERROR: GROQ_API_KEY Python tak nahi pahunchi! GitHub Secrets ya YAML file check karein.")
            return "Bhaiyo, naya gaming update aane wala hai! Taiyaar ho jao. 🎮🔥 #Gaming #BGMI #FreeFire #GTA6"

        topics = [
            "a funny meme story or relatable situation about BGMI campers",
            "latest news, leaks or exciting rumors about GTA 6",
            "pro tips and secret tricks for Free Fire players",
            "a 'Reaction Poll' asking Indian gamers to choose between BGMI and Free Fire. Ask to use Facebook reactions (Like 👍, Heart ❤️)."
        ]
        chosen_topic = random.choice(topics)
        
        prompt = (
            f"Write a viral Hinglish (Hindi + English) gaming Facebook post about: {chosen_topic}. "
            "Keep it funny, highly engaging, use lots of emojis and trending hashtags. Target audience: Indian gamers."
        )
        
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama3-8b-8192", 
            "messages": [{"role": "user", "content": prompt}]
        }
        
        print("Groq AI se naya content mang rahe hain...")
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        
        # DEBUG CHECK 2: Kya Groq ne API key reject ki?
        if 'error' in result:
            print(f"❌ GROQ KA ASLI ERROR: {result['error']}")
            return "Bhaiyo, naya gaming update aane wala hai! Taiyaar ho jao. 🎮🔥 #Gaming #BGMI #FreeFire #GTA6"
        
        return result['choices'][0]['message']['content']
        
    except Exception as e:
        print(f"Python Execution Error: {e}")
        return "Bhaiyo, naya gaming update aane wala hai! Taiyaar ho jao. 🎮🔥 #Gaming #BGMI #FreeFire #GTA6"

def post_to_facebook():
    page_id = '318640404662743' 
    system_token = os.environ.get('FB_TOKEN')
    
    token_url = f"https://graph.facebook.com/{page_id}?fields=access_token&access_token={system_token}"
    token_response = requests.get(token_url).json()
    
    if 'access_token' in token_response:
        page_token = token_response['access_token']
        print("Success: Page Access Token mil gaya!")
    else:
        print(f"Token Error: {token_response}")
        return
    
    url = f"https://graph.facebook.com/{page_id}/feed"
    message = get_ai_content()
    
    payload = {'message': message, 'access_token': page_token}
    
    r = requests.post(url, data=payload)
    print(f"Facebook Response: {r.json()}")

if __name__ == "__main__":
    post_to_facebook()

import requests
import os
import random
import urllib.parse

def get_ai_data():
    try:
        api_key = os.environ.get('GROQ_API_KEY')
        
        if not api_key:
            print("❌ GROQ_API_KEY nahi mili!")
            return "Bhaiyo, taiyaar ho jao nayi gaming stream ke liye! 🎮🔥", "https://image.pollinations.ai/prompt/neon%20gaming%20controller%203d?width=1080&height=1080&nologo=true"

        topics = [
            "BGMI campers funny situation",
            "GTA 6 exciting leaks",
            "Free Fire pro headshot tricks",
            "Indian gamers slow internet struggle"
        ]
        chosen_topic = random.choice(topics)
        
        # 1. Groq se Hinglish Caption Likhwana
        caption_prompt = (
            f"Topic: {chosen_topic}. "
            "CRITICAL RULE: You MUST write the entire post strictly in 'Hinglish' (Hindi language written in English alphabet). "
            "DO NOT write in pure English. "
            "Example style: 'Bhaiyo aur behno, aaj BGMI mein kya hi game hua! 😂' "
            "Keep it very funny, engaging, use lots of emojis and trending hashtags."
        )
        
        url_groq = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama-3.1-8b-instant", 
            "messages": [{"role": "user", "content": caption_prompt}]
        }
        
        print("Groq AI se Hinglish caption mang rahe hain...")
        response = requests.post(url_groq, headers=headers, json=data)
        result = response.json()
        caption = result['choices'][0]['message']['content']
        
        # 2. Free AI se Image Generate karna (Pollinations AI)
        print("AI Image ka URL bana rahe hain...")
        image_prompt = f"3D high quality cartoon style concept art about {chosen_topic} video game, highly detailed, colorful, vibrant"
        
        # Text ko URL format mein convert karna (spaces ko %20 banana)
        safe_prompt = urllib.parse.quote(image_prompt)
        
        # 1080x1080 (Square HD Image)
        image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1080&height=1080&nologo=true"
        
        return caption, image_url
        
    except Exception as e:
        print(f"Error: {e}")
        return "Bhaiyo, taiyaar ho jao nayi gaming stream ke liye! 🎮🔥", "https://image.pollinations.ai/prompt/neon%20gaming%20controller%203d?width=1080&height=1080&nologo=true"

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
    
    # AI se Text aur Image URL dono lena
    caption, image_url = get_ai_data()
    
    # NAYA DARWAZA: '/feed' ki jagah ab hum '/photos' use kar rahe hain
    url = f"https://graph.facebook.com/{page_id}/photos"
    
    # Payload mein 'message' (Text) aur 'url' (Photo ka link) dono bhejna
    payload = {
        'message': caption, 
        'url': image_url,
        'access_token': page_token
    }
    
    print("Facebook par Photo upload ho rahi hai...")
    r = requests.post(url, data=payload)
    print(f"Facebook Response: {r.json()}")

if __name__ == "__main__":
    post_to_facebook()

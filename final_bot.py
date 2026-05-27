import requests
import os
import random
import urllib.parse
from PIL import Image, ImageDraw, ImageFont
import io
import time

def get_live_news():
    print("Middleman (RSS2JSON) ke zariye Reddit ki Live News nikal rahe hain...")
    try:
        # The Middleman Trick: Reddit RSS ko JSON mein convert karna bina API key ke
        rss_url = "https://www.reddit.com/r/gamingnews/.rss"
        api_url = f"https://api.rss2json.com/v1/api.json?rss_url={urllib.parse.quote(rss_url)}"
        
        r = requests.get(api_url)
        if r.status_code == 200:
            data = r.json()
            # Sabse pehli (latest) khabar uthana
            latest_news = data['items'][0]['title']
            return latest_news
        else:
            return None
    except Exception as e:
        print(f"News Fetch Error: {e}")
        return None

def get_ai_data():
    api_key = os.environ.get('GROQ_API_KEY')
    
    if not api_key:
        print("Error: API Key missing!")
        return "Bhaiyo, taiyaar ho jao nayi gaming stream ke liye! 🎮🔥", None

    # Step 1: Live News fetch karne ki koshish
    live_news = get_live_news()
    
    # Step 2: 50-50 Logic - Ya toh Live News, ya phir humari 50-topic wali list
    # random.choice([True, False]) ek sikka (coin) uchhalta hai
    if live_news and random.choice([True, False]):
        chosen_topic = f"Breaking Gaming News: {live_news}"
        print(f"🔥 Aaj ka Topic (LIVE NEWS): {chosen_topic}")
    else:
        # Humara 50 Topics ka Massive Backup
        topics = [
            "BGMI random teammates doing stupid things",
            "Landing at Pochinki and getting no gun in BGMI",
            "The fear of the Red Zone in BGMI",
            "Finding a flare gun but teammates steal the loot",
            "Getting killed by a snake (camper) in the last circle of Sanhok",
            "The feeling of getting a Chicken Dinner after a 10-match losing streak",
            "When your Ping goes to 999ms during a 1v4 clutch",
            "Reviving a teammate in the blue zone",
            "Looting a drop but getting sniped instantly",
            "Rushing a squad house with just a shotgun",
            "Trying to hit a perfect one-tap headshot in Free Fire",
            "When someone destroys your Gloo Wall in Free Fire",
            "DJ Alok vs Chrono funny debates",
            "Landing at Peak in Bermuda map and dying in 10 seconds",
            "Rank push struggles in Free Fire Heroic tier",
            "When your teammate loots your bounty token",
            "Playing clash squad randoms and teammates go offline",
            "The stress of 1v1 custom room matches in FF",
            "Missing the airdrop by 1 inch in FF",
            "Using a sniper but missing all shots",
            "Opening a 110+ OVR pack in FC Mobile and getting a useless player",
            "When script goes against you in FC Mobile H2H match",
            "Scoring a last-minute 90th-minute header in FC Mobile",
            "Saving millions of coins to buy your favorite striker",
            "When the opponent celebrates after scoring a tap-in goal",
            "Upgrading a player in FC Mobile and running out of fodder",
            "The lag when you are about to shoot a penalty in H2H",
            "Building a full icon squad but still losing to a silver team",
            "The pain of Market tax in FC Mobile",
            "Waiting for Thursday reset for new events",
            "Waiting for GTA 6 to release so we can finally rest",
            "GTA 6 trailer leaks funny reaction",
            "Minecraft gamers building a dirt house on day 1",
            "Valorant players getting toxic over voice chat",
            "Missing easy shots with an Operator in Valorant",
            "Buying a gaming PC but only playing low graphics games",
            "RGB lights make my PC 100% faster joke",
            "GTA 5 driving mechanics vs real life",
            "When a console player tries mouse and keyboard for the first time",
            "Skyrim mods crashing the game funny moment",
            "Having a B.Tech semester exam tomorrow but doing a 3 AM rank push",
            "When hostel Wi-Fi disconnects right in the middle of a clutch",
            "Engineering students fixing coding bugs vs fixing ping issues",
            "Telling parents 'This game cannot be paused'",
            "Playing games on a laptop that sounds like a jet engine",
            "When you use your engineering brain to calculate grenade trajectory but still die",
            "Submitting assignment at 11:59 PM and opening BGMI at 12:00 AM",
            "Trying to balance CGPA and K/D Ratio",
            "When your non-gamer friend tries to play a racing game",
            "The ultimate dream of buying a high-end gaming setup after getting a job"
        ]
        chosen_topic = random.choice(topics)
        print(f"😂 Aaj ka Topic (GAMER STRUGGLE): {chosen_topic}")

    # Step 3: Text ko Unique rakhne ka naya prompt
    caption_prompt = (
        f"Topic: '{chosen_topic}'. "
        "CRITICAL RULE: Act as a funny Indian gamer 'Engineers Gamer'. Write a highly engaging Facebook post strictly in 'Hinglish'. "
        "CRITICAL RULE 2: Make this post 100% unique and fresh. Do not repeat old jokes. "
        "Keep it very funny, relatable, use lots of emojis and trending hashtags."
    )
    
    url_groq = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    
    # Temperature 0.8 rakha hai taaki AI har baar naye words soche (100% unique)
    data = {"model": "llama-3.1-8b-instant", "messages": [{"role": "user", "content": caption_prompt}], "temperature": 0.8}
    
    print("Groq AI se 100% unique Hinglish caption banwa rahe hain...")
    caption = requests.post(url_groq, headers=headers, json=data).json()['choices'][0]['message']['content']
    
    # Step 4: Image ko Unique rakhne ka Seed Logic
    print("AI Image ka URL bana rahe hain (REALISTIC STYLE & 100% UNIQUE)...")
    unique_seed = int(time.time()) + random.randint(1, 100000)
    
    image_prompt = f"Hyper-realistic 8k resolution cinematic lighting photorealistic game graphics render of: {chosen_topic}. Unreal Engine 5 style, highly detailed textures, vibrant."
    safe_prompt = urllib.parse.quote(image_prompt)
    
    # URL ke end mein '&seed=...' laga diya
    image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1080&height=1080&nologo=true&seed={unique_seed}"
    
    return caption, image_url

def add_watermark(image_url):
    print("Image download karke 'Engineers Gamer' ka watermark laga rahe hain...")
    try:
        img_data = requests.get(image_url).content
        img = Image.open(io.BytesIO(img_data))
        
        draw = ImageDraw.Draw(img)
        watermark_text = " Engineers Gamer "
        
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 45)
        except:
            font = ImageFont.load_default()
        
        width, height = img.size
        draw.rectangle([(0, height - 70), (width, height)], fill=(0, 0, 0, 180))
        draw.text((20, height - 60), watermark_text, fill="white", font=font)
        
        img_path = "watermarked_image.jpg"
        img.save(img_path)
        return img_path
    except Exception as e:
        print(f"Watermark Error: {e}")
        return None

def post_to_facebook():
    page_id = '318640404662743' 
    system_token = os.environ.get('FB_TOKEN')
    
    token_url = f"https://graph.facebook.com/{page_id}?fields=access_token&access_token={system_token}"
    page_token = requests.get(token_url).json().get('access_token')
    
    if not page_token:
        print("Token Error!")
        return

    caption, image_url = get_ai_data()
    local_image_path = add_watermark(image_url)
    
    url = f"https://graph.facebook.com/{page_id}/photos"
    
    if local_image_path:
        print("Facebook par Watermark wali photo upload ho rahi hai...")
        payload = {'message': caption, 'access_token': page_token}
        files = {'source': open(local_image_path, 'rb')}
        r = requests.post(url, data=payload, files=files)
    else:
        print("Watermark fail hua, direct URL bhej rahe hain...")
        payload = {'message': caption, 'url': image_url, 'access_token': page_token}
        r = requests.post(url, data=payload)
        
    print(f"Facebook Response: {r.json()}")

if __name__ == "__main__":
    post_to_facebook()

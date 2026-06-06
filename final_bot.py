import requests
import os
import random
import urllib.parse
from PIL import Image, ImageDraw, ImageFont
import time

def get_live_news():
    print("Middleman (RSS2JSON) ke zariye Reddit ki Live News nikal rahe hain...")
    try:
        rss_url = "https://www.reddit.com/r/gamingnews/.rss"
        api_url = f"https://api.rss2json.com/v1/api.json?rss_url={urllib.parse.quote(rss_url)}"
        
        r = requests.get(api_url, timeout=15)
        if r.status_code == 200:
            data = r.json()
            latest_news = data['items'][0]['title']
            return latest_news
        else:
            return None
    except Exception as e:
        print(f"News Fetch Error: {e}")
        return None

def get_ai_caption_and_prompt():
    api_key = os.environ.get('GROQ_API_KEY')
    
    live_news = get_live_news()
    choice = random.choices(['news', 'topic'], weights=[25, 75], k=1)[0]
    
    if live_news and choice == 'news':
        chosen_topic = f"Breaking Gaming News: {live_news}"
        print(f"🔥 Aaj ka Topic (LIVE NEWS): {chosen_topic}")
    else:
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
        print(f"😂 Aaj ka Topic: {chosen_topic}")

    caption = f"Bhaiyo kya scene hai? {chosen_topic} 😂🔥\n\n#ErAshuGaming #GamingLife #Esports"
    
    if api_key:
        caption_prompt = (
            f"Topic: '{chosen_topic}'.\n\n"
            "Act as a funny Indian gaming meme page admin ('Engineers Gamer'). Write a short, 2-line Facebook caption in NATURAL HINGLISH (Hindi language written in English alphabet mixed with English gaming words).\n\n"
            "EXAMPLES OF GOOD HINGLISH:\n"
            "- 'Bhai yaar yeh ping issue ne dimaag kharab kar diya hai! Kis kis ke sath aisa hota hai? 😂'\n"
            "- 'Relatable pro max! Jab random teammate loot chura le toh kaisa feel hota hai bhaiyo? 💀👇'\n"
            "- 'Exam kal hai aur hum yahan rank push kar rahe hain. 🥲 Comment your rank!'\n\n"
            "CRITICAL RULES:\n"
            "1. DO NOT use formal or weird translated Hindi. Talk like a normal Indian gamer.\n"
            "2. Keep it very short (Max 2 lines).\n"
            "3. End with an engaging question asking people to comment (e.g., 'Sach batao kis kis ke sath hua hai? 👇').\n"
            "4. DO NOT output any extra text, headings, or notes. ONLY the caption and 3-4 hashtags."
        )
        try:
            url_groq = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            data = {"model": "llama-3.1-8b-instant", "messages": [{"role": "user", "content": caption_prompt}], "temperature": 0.7}
            print("Groq AI se Natural Hinglish caption banwa rahe hain...")
            res = requests.post(url_groq, headers=headers, json=data, timeout=15)
            caption = res.json()['choices'][0]['message']['content']
        except Exception as e:
            print(f"Groq Caption Error: {e}")

    visual_styles = [
        "first-person POV in-game action screenshot, vibrant lighting, highly detailed",
        "cinematic movie poster style, dramatic epic low angle, Unreal Engine 5",
        "e-sports tournament stage setting, neon RGB lights, massive crowd background, 8k",
        "dark and gritty cinematic render, intense shadows, photorealistic",
        "vibrant concept art style, highly detailed gaming environment, dynamic composition"
    ]
    random_style = random.choice(visual_styles)
    
    image_prompt = f"{chosen_topic}, {random_style}, masterpiece, trending on artstation"
    return caption, image_prompt

# 🔥 NAYA NEVER-FAIL IMAGE DOWNLOAD SYSTEM
def generate_robust_photo(prompt):
    print(f"🎨 Image Prompt: {prompt}")
    safe_prompt = urllib.parse.quote(prompt)
    unique_seed = int(time.time()) + random.randint(1, 100000)
    
    # FIX: Removed width, height, and nologo parameters to avoid Error 402
    img_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?seed={unique_seed}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0"
    }

    try:
        r = requests.get(img_url, headers=headers, timeout=20)
        if r.status_code == 200:
            with open("photo_temp.jpg", "wb") as f: 
                f.write(r.content)
            print("✅ Try 1 Success: AI Image Downloaded!")
            return True
    except:
        pass

    print("⚠️ AI Blocked (402). Backup System Active: Downloading HQ Gaming Photo...")
    fallback_images = [
        "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=1080&h=1080&fit=crop", 
        "https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=1080&h=1080&fit=crop", 
        "https://images.unsplash.com/photo-1552820728-8b83bb6b7738?w=1080&h=1080&fit=crop", 
        "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=1080&h=1080&fit=crop"  
    ]
    try:
        r = requests.get(random.choice(fallback_images), timeout=20)
        if r.status_code == 200:
            with open("photo_temp.jpg", "wb") as f:
                f.write(r.content)
            print("✅ Try 2 Success: Backup Wallpaper Downloaded!")
            return True
    except:
        pass

    print("⚠️ Wallpaper bhi fail. Solid background use kar rahe hain.")
    img = Image.new('RGB', (1080, 1080), color=(25, 25, 25))
    img.save('photo_temp.jpg')
    print("✅ Try 3 Success: Basic Background Ready!")
    return True

def add_watermark():
    print("Image ko 1080x1080 me fix karke 'Er Ashu Gaming' ka watermark laga rahe hain...")
    
    # Image resize ki jarurat idhar puri ki gayi hai
    img = Image.open("photo_temp.jpg")
    img = img.resize((1080, 1080), Image.Resampling.LANCZOS)
    
    draw = ImageDraw.Draw(img)
    width, height = img.size
    
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 45)
    except:
        font = ImageFont.load_default()
    
    draw.rectangle([(0, height - 70), (width, height)], fill=(0, 0, 0, 180))
    draw.text((20, height - 60), " ER ASHU GAMING ", fill="white", font=font)
    
    img_path = "watermarked_image.jpg"
    img.save(img_path)
    return img_path

def post_to_facebook():
    page_id = '318640404662743' 
    system_token = os.environ.get('FB_TOKEN')
    
    try:
        token_url = f"https://graph.facebook.com/{page_id}?fields=access_token&access_token={system_token}"
        token_response = requests.get(token_url).json()
        page_token = token_response.get('access_token')
        
        if not page_token:
            print("Token Error!")
            return
    except Exception as e:
        print(f"Facebook Token Fetch Error: {e}")
        return

    # Data Generate Karo
    caption, image_prompt = get_ai_caption_and_prompt()
    
    # Image Generate aur Upload Karo
    if generate_robust_photo(image_prompt):
        local_image_path = add_watermark()
        url = f"https://graph.facebook.com/{page_id}/photos"
        
        print("🚀 Facebook par Watermark wali photo upload ho rahi hai...")
        payload = {'message': caption, 'access_token': page_token}
        
        with open(local_image_path, 'rb') as f:
            files = {'source': f}
            r = requests.post(url, data=payload, files=files)
            
        print(f"✅ Facebook Response: {r.json()}")
    else:
        print("❌ Image generation poori tarah se fail ho gayi.")

if __name__ == "__main__":
    post_to_facebook()

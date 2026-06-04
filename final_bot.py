import requests
import os
import random
import urllib.parse
from PIL import Image, ImageDraw, ImageFont
import time
import textwrap

# Ignore SSL warnings caused by direct IP routing
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_live_news():
    print("Middleman (RSS2JSON) ke zariye Reddit ki Live News nikal rahe hain...")
    try:
        rss_url = "https://www.reddit.com/r/gamingnews/.rss"
        api_url = f"https://api.rss2json.com/v1/api.json?rss_url={urllib.parse.quote(rss_url)}"
        
        r = requests.get(api_url)
        if r.status_code == 200:
            data = r.json()
            return data['items'][0]['title']
        return None
    except Exception as e:
        print(f"News Fetch Error: {e}")
        return None

def generate_ai_image(prompt):
    hf_token = os.environ.get('HF_TOKEN')
    if not hf_token:
        print("❌ ERROR: GitHub Secrets mein HF_TOKEN nahi mila!")
        return False

    # 🔥 DIRECT IP ROUTING FOR PHOTOS TOO
    API_URL = "https://18.243.141.112/models/Lykon/dreamshaper-xl-v2-turbo"
    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Host": "api-inference.huggingface.co"
    }
    payload = {"inputs": prompt}

    max_retries = 3
    for attempt in range(max_retries):
        print(f"Hugging Face API (Direct IP) ko request bhej rahe hain (Attempt {attempt + 1}/3)...")
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=60, verify=False)
            
            if response.status_code == 200:
                with open("photo_temp.jpg", "wb") as f:
                    f.write(response.content)
                img = Image.open("photo_temp.jpg")
                img = img.resize((1080, 1080), Image.Resampling.LANCZOS)
                img.save("photo_temp.jpg")
                print("✅ 8K Photo successfully generated via Direct IP!")
                return True
            
            elif response.status_code == 503:
                print("⏳ Model load ho raha hai (503). 15 seconds wait...")
                time.sleep(15)
            else:
                print(f"⚠️ API Error: {response.status_code}. Retrying...")
                time.sleep(5)
                
        except Exception as e:
            print(f"⚠️ Direct IP failed ({e}), backup domain try kar rahe hain...")
            try:
                BACKUP_URL = "https://api-inference.huggingface.co/models/Lykon/dreamshaper-xl-v2-turbo"
                backup_headers = {"Authorization": f"Bearer {hf_token}"}
                response = requests.post(BACKUP_URL, headers=backup_headers, json=payload, timeout=40)
                if response.status_code == 200:
                    with open("photo_temp.jpg", "wb") as f:
                        f.write(response.content)
                    print("✅ Photo generated via Backup Domain!")
                    return True
            except Exception as backup_err:
                print(f"❌ Backup Domain bhi fail hua: {backup_err}")
            time.sleep(5)
            
    return False

def add_watermark(image_path):
    print("Photo par watermark laga rahe hain...")
    try:
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        watermark_text = " Er Ashu Gaming "
        
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 45)
        except:
            font = ImageFont.load_default()
        
        width, height = img.size
        draw.rectangle([(0, height - 70), (width, height)], fill=(0, 0, 0, 180))
        draw.text((20, height - 60), watermark_text, fill="white", font=font)
        
        watermarked_path = "watermarked_photo.jpg"
        img.save(watermarked_path)
        return watermarked_path
    except Exception as e:
        print(f"❌ Watermark Error: {e}")
        return None

def post_to_facebook():
    api_key = os.environ.get('GROQ_API_KEY')
    if not api_key:
        print("Error: GROQ_API_KEY missing!")
        return

    live_news = get_live_news()
    choice = random.choices(['news', 'topic'], weights=[25, 75], k=1)[0]
    
    if live_news and choice == 'news':
        chosen_topic = f"Breaking Gaming News: {live_news}"
        print(f"🔥 Aaj ka Topic (LIVE NEWS): {chosen_topic}")
    else:
        topics = [
            "BGMI random teammates doing stupid things",
            "Landing at Pochinki and getting no gun in BGMI",
            "The feeling of getting a Chicken Dinner after a 10-match losing streak",
            "When your Ping goes to 999ms during a 1v4 clutch",
            "Trying to hit a perfect one-tap headshot in Free Fire",
            "Rank push struggles in Free Fire Heroic tier",
            "When script goes against you in FC Mobile H2H match",
            "Waiting for GTA 6 to release so we can finally rest",
            "Minecraft gamers building a dirt house on day 1",
            "When hostel Wi-Fi disconnects right in the middle of a clutch"
        ]
        chosen_topic = random.choice(topics)
        print(f"😂 Aaj ka Topic: {chosen_topic}")

    caption_prompt = (
        f"Topic: '{chosen_topic}'.\n\n"
        "Act as a funny Indian gaming meme page admin ('Engineers Gamer'). Write a short, 2-line Facebook caption in NATURAL HINGLISH (Hindi language written in English alphabet mixed with English gaming words).\n\n"
        "RULES:\n"
        "1. DO NOT use formal or weird translated Hindi.\n"
        "2. Keep it very short (Max 2 lines) and end with an engaging question.\n"
        "3. ONLY the caption and 3-4 hashtags."
    )
    
    url_groq = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {"model": "llama-3.1-8b-instant", "messages": [{"role": "user", "content": caption_prompt}], "temperature": 0.7}
    
    print("Groq AI se Natural Hinglish caption banwa rahe hain...")
    try:
        caption = requests.post(url_groq, headers=headers, json=data).json()['choices'][0]['message']['content']
    except Exception as e:
        print(f"❌ Caption Error: {e}")
        return

    visual_styles = ["first-person POV in-game action screenshot", "cinematic movie poster style", "e-sports tournament stage setting"]
    image_prompt = f"{chosen_topic}, {random.choice(visual_styles)}, masterpiece, trending on artstation"
    
    if not generate_ai_image(image_prompt):
        print("🛑 UPLOAD CANCELLED: Hugging Face se image nahi ban payi.")
        return

    watermarked_image = add_watermark("photo_temp.jpg")
    if not watermarked_image:
        print("🛑 UPLOAD CANCELLED: Watermark error.")
        return

    page_id = '318640404662743' 
    system_token = os.environ.get('FB_TOKEN')
    
    token_url = f"https://graph.facebook.com/{page_id}?fields=access_token&access_token={system_token}"
    try:
        page_token = requests.get(token_url).json().get('access_token')
    except Exception as e:
        print(f"❌ Token fetch error: {e}")
        return
    
    if not page_token:
        print("Token Error!")
        return

    url = f"https://graph.facebook.com/{page_id}/photos"
    print("✅ Facebook par photo upload ho rahi hai...")
    payload = {'message': caption, 'access_token': page_token}
    
    try:
        with open(watermarked_image, 'rb') as img_file:
            files = {'source': img_file}
            r = requests.post(url, data=payload, files=files)
            print(f"Upload Response: {r.json()}")
    except Exception as e:
        print(f"❌ Upload Error: {e}")

if __name__ == "__main__":
    post_to_facebook()
    

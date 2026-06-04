import requests
import os
import random
import urllib.parse
from PIL import Image, ImageDraw, ImageFont
import time

def get_live_news():
    try:
        rss_url = "https://www.reddit.com/r/gamingnews/.rss"
        api_url = f"https://api.rss2json.com/v1/api.json?rss_url={urllib.parse.quote(rss_url)}"
        r = requests.get(api_url, timeout=10)
        if r.status_code == 200: return r.json()['items'][0]['title']
        return None
    except: return None

def generate_pure_ai_image(prompt):
    realistic_prompt = f"mdjrny-v4 style, {prompt}, realistic gaming setup action screenshot, photorealistic, 4k cinematic lighting, highly detailed"
    safe_prompt = urllib.parse.quote(realistic_prompt)
    seed = random.randint(1, 1000000)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://pollinations.ai/'
    }
    
    url_direct = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1080&height=1080&seed={seed}"
    url_proxy = f"https://wsrv.nl/?url=image.pollinations.ai/prompt/{safe_prompt}%3Fwidth%3D1080%26height%3D1080%26seed%3D{seed}"
    url_hercai = f"https://hercai.onrender.com/v3/text2image?prompt={safe_prompt}"

    print("🕵️ Route 1: Fake Browser Headers try kar rahe hain...")
    try:
        r1 = requests.get(url_direct, headers=headers, timeout=30)
        if r1.status_code == 200:
            with open("photo_temp.jpg", "wb") as f: f.write(r1.content)
            img = Image.open("photo_temp.jpg").resize((1080, 1080), Image.Resampling.LANCZOS)
            img.save("photo_temp.jpg")
            print("✅ Route 1 Successful!")
            return True
    except: pass
    
    time.sleep(2)
    print("🌐 Route 2: Netherlands Proxy se IP Ban bypass kar rahe hain...")
    try:
        r2 = requests.get(url_proxy, headers=headers, timeout=30)
        if r2.status_code == 200:
            with open("photo_temp.jpg", "wb") as f: f.write(r2.content)
            img = Image.open("photo_temp.jpg").resize((1080, 1080), Image.Resampling.LANCZOS)
            img.save("photo_temp.jpg")
            print("✅ Route 2 Successful!")
            return True
    except: pass
    
    time.sleep(2)
    print("🤖 Route 3: Hercai AI Alternate Engine use kar rahe hain...")
    try:
        r3 = requests.get(url_hercai, headers=headers, timeout=30)
        if r3.status_code == 200:
            data = r3.json()
            if "url" in data and data["url"]:
                img_resp = requests.get(data["url"], headers=headers, timeout=30)
                if img_resp.status_code == 200:
                    with open("photo_temp.jpg", "wb") as f: f.write(img_resp.content)
                    img = Image.open("photo_temp.jpg").resize((1080, 1080), Image.Resampling.LANCZOS)
                    img.save("photo_temp.jpg")
                    print("✅ Route 3 Successful!")
                    return True
    except: pass

    return False

def add_watermark(image_path):
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
    except:
        return image_path

def post_to_facebook():
    api_key = os.environ.get('GROQ_API_KEY')
    if not api_key: return

    live_news = get_live_news()
    choice = random.choices(['news', 'topic'], weights=[25, 75], k=1)[0]
    
    if live_news and choice == 'news': chosen_topic = f"Breaking Gaming News: {live_news}"
    else:
        topics = [
            "BGMI random teammates doing stupid things",
            "Landing at Pochinki and getting no gun in BGMI",
            "The feeling of getting a Chicken Dinner after a 10-match losing streak",
            "When your Ping goes to 999ms during a 1v4 clutch",
            "Trying to hit a perfect one-tap headshot in Free Fire",
            "Rank push struggles in Free Fire Heroic tier",
            "When script goes against you in FC Mobile H2H match",
            "Waiting for GTA 6 to release so we can finally rest"
        ]
        chosen_topic = random.choice(topics)

    caption_prompt = f"Topic: '{chosen_topic}'. Write a short, 2-line Facebook caption in funny gamer NATURAL HINGLISH. End with an engaging question and 3 hashtags. No extra prose."
    
    try:
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        data = {"model": "llama-3.1-8b-instant", "messages": [{"role": "user", "content": caption_prompt}], "temperature": 0.7}
        caption = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data).json()['choices'][0]['message']['content']
    except:
        caption = f"Kya bolte ho lala? {chosen_topic} 😂🔥\n\n#EngineersGamer"

    if not generate_pure_ai_image(chosen_topic):
        print("🛑 UPLOAD CANCELLED: AI Image nahi bani. Strict Rule enforced.")
        return

    watermarked_image = add_watermark("photo_temp.jpg")

    page_id = '318640404662743' 
    system_token = os.environ.get('FB_TOKEN')
    try:
        page_token = requests.get(f"https://graph.facebook.com/{page_id}?fields=access_token&access_token={system_token}").json().get('access_token')
        if page_token:
            print("✅ Facebook par photo upload ho rahi hai...")
            with open(watermarked_image, 'rb') as img_file:
                requests.post(f"https://graph.facebook.com/{page_id}/photos", data={'message': caption, 'access_token': page_token}, files={'source': img_file})
                print("✅ Uploaded to Facebook!")
    except Exception as e:
        print(f"❌ Upload Error: {e}")

if __name__ == "__main__":
    post_to_facebook()
    

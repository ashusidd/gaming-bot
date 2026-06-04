import requests
import os
import random
import urllib.parse
from PIL import Image, ImageDraw, ImageFont

def get_live_news():
    try:
        rss_url = "https://www.reddit.com/r/gamingnews/.rss"
        api_url = f"https://api.rss2json.com/v1/api.json?rss_url={urllib.parse.quote(rss_url)}"
        r = requests.get(api_url, timeout=10)
        if r.status_code == 200: return r.json()['items'][0]['title']
        return None
    except: return None

def generate_pure_ai_image(prompt):
    # Pollinations AI: Fast, Stable, No Token, No 503 Errors
    print(f"🚀 Generating AI Image for: {prompt}")
    safe_prompt = prompt.replace(" ", "%20")
    url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1080&height=1080&seed={random.randint(1,9999)}"
    try:
        response = requests.get(url, timeout=60)
        if response.status_code == 200:
            with open("photo_temp.jpg", "wb") as f: f.write(response.content)
            return True
    except Exception as e:
        print(f"❌ Image Gen Error: {e}")
        return False

def add_watermark(image_path):
    try:
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        # Windows/Linux font path (Default fallback)
        try:
            font = ImageFont.truetype("arial.ttf", 45) # Windows ke liye
        except:
            font = ImageFont.load_default()
        
        width, height = img.size
        draw.rectangle([(0, height - 70), (width, height)], fill=(0, 0, 0, 180))
        draw.text((20, height - 60), " ER ASHU GAMING ", fill="white", font=font)
        
        img.save("watermarked_photo.jpg")
        return "watermarked_photo.jpg"
    except: return image_path

def post_to_facebook():
    api_key = os.environ.get('GROQ_API_KEY')
    live_news = get_live_news()
    choice = random.choices(['news', 'topic'], weights=[25, 75], k=1)[0]
    
    if live_news and choice == 'news': chosen_topic = f"Breaking Gaming News: {live_news}"
    else:
        topics = ["BGMI random teammates", "Pochinki landing", "1v4 clutch stress", "Rank push struggles"]
        chosen_topic = random.choice(topics)

    # Groq Caption Logic
    caption = f"Kya bolte ho lala? {chosen_topic} 😂🔥\n\n#ErAshuGaming"
    if api_key:
        try:
            data = {"model": "llama-3.1-8b-instant", "messages": [{"role": "user", "content": f"Write funny Hinglish caption for: {chosen_topic}"}]}
            caption = requests.post("https://api.groq.com/openai/v1/chat/completions", headers={"Authorization": f"Bearer {api_key}"}, json=data).json()['choices'][0]['message']['content']
        except: pass

    if generate_pure_ai_image(chosen_topic):
        img_path = add_watermark("photo_temp.jpg")
        token = os.environ.get('FB_TOKEN')
        page_id = '318640404662743'
        
        with open(img_path, 'rb') as f:
            requests.post(f"https://graph.facebook.com/{page_id}/photos", data={'message': caption, 'access_token': token}, files={'source': f})
        print("✅ Posted successfully to FB!")

if __name__ == "__main__":
    post_to_facebook()

import requests
import os
import urllib.parse
from PIL import Image, ImageDraw, ImageFont
import io

def get_live_news():
    print("Reddit se live gaming news nikal rahe hain...")
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get('https://www.reddit.com/r/gamingnews/new.json?limit=1', headers=headers)
        data = r.json()
        latest_news = data['data']['children'][0]['data']['title']
        print(f"Taaza Khabar Mili: {latest_news}")
        return latest_news
    except Exception as e:
        print(f"News Error: {e}")
        return "BGMI and GTA 6 exciting latest rumors" # Fallback topic

def get_ai_data(news_topic):
    api_key = os.environ.get('GROQ_API_KEY')
    
    if not api_key:
        return "Bhaiyo, taiyaar ho jao nayi gaming stream ke liye! 🎮🔥", None

    # 1. Groq se Hinglish Caption banwana
    caption_prompt = (
        f"Latest Gaming News: '{news_topic}'. "
        "CRITICAL RULE: Act as a funny Indian gamer. Write a Facebook post about this news strictly in 'Hinglish' (Hindi language written in English alphabet). "
        "DO NOT write in pure English. "
        "Example style: 'Bhaiyo aur behno, ek bohot tagdi news aayi hai nikal ke... 😂' "
        "Keep it highly engaging, funny, use emojis and trending hashtags."
    )
    
    url_groq = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {"model": "llama-3.1-8b-instant", "messages": [{"role": "user", "content": caption_prompt}]}
    
    print("Groq AI se Hinglish caption banwa rahe hain...")
    caption = requests.post(url_groq, headers=headers, json=data).json()['choices'][0]['message']['content']
    
    # ---------------------------------------------------------
    # UPDATED: Realistic Image Prompt
    # ---------------------------------------------------------
    print("AI Image ka URL bana rahe hain (REALISTIC STYLE)...")
    # Yahan humne style change karke hyper-realistic aur Unreal Engine 5 add kiya hai
    image_prompt = f"Hyper-realistic 8k resolution cinematic lighting photorealistic game graphics render of: {news_topic}. Unreal Engine 5 style, ray tracing, highly detailed textures, realistic colors."
    
    safe_prompt = urllib.parse.quote(image_prompt)
    image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1080&height=1080&nologo=true"
    
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

    # A. Live News Lena
    news_topic = get_live_news()
    
    # B. AI se Text aur Image Link Lena (Now Realistic)
    caption, image_url = get_ai_data(news_topic)
    
    # C. Image par Watermark lagana
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

import requests
import os
import random
import json
import time # Ye rukne ke kaam aayega
import urllib.parse
import textwrap
from PIL import Image
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip, AudioFileClip

# 1. Topic wala function (Same hai)
def get_topic():
    try:
        with open("topics.json", "r+") as f:
            data = json.load(f)
            remaining = [t for t in data["all_topics"] if t not in data["used_topics"]]
            if not remaining:
                data["used_topics"] = []
                remaining = data["all_topics"]
            topic = random.choice(remaining)
            data["used_topics"].append(topic)
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
        return topic
    except Exception as e:
        print(f"Topic Error: {e}")
        return "Free Fire vs PUBG: Choose Your Path"

# 2. Music wala function (Same hai)
def get_random_music():
    music_folder = "music"
    if os.path.exists(music_folder):
        files = [f for f in os.listdir(music_folder) if f.endswith(".mp3")]
        if files:
            return os.path.join(music_folder, random.choice(files))
    return None

# 3. Prompt Generator (Isme 402 error fix kiya)
def get_safe_visual_prompt(topic):
    api_key = os.environ.get('GROQ_API_KEY')
    fallback_prompt = f"split screen gaming comparison, two warriors fighting, bright colors, 8k resolution"
    
    if not api_key: 
        return fallback_prompt

    try:
        time.sleep(5) # API ko hit karne se pehle 5 second ka aaram diya (Spam prevention)
        prompt_instruction = (
            f"Create a short, vivid visual description for this gaming topic: '{topic}'. "
            "CRITICAL RULE: DO NOT use any copyrighted game names (like PUBG, Valorant, Free Fire) "
            "or specific character names. Use generic terms like 'wind ninja', "
            "'cyber soldier', 'vampire warrior', etc. Keep it under 15 words."
        )
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        data = {"model": "llama-3.1-8b-instant", "messages": [{"role": "user", "content": prompt_instruction}]}
        res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data, timeout=10)
        
        clean_desc = res.json()['choices'][0]['message']['content'].strip()
        clean_desc = clean_desc.replace('"', '').replace("'", "") 
        return f"split screen comparison, {clean_desc}, epic gaming 3d render, 8k resolution"
    except Exception as e:
        return fallback_prompt

# 4. Background Image (Borders aur 402 dono yahan fix kiye)
def get_background_image(safe_prompt):
    # FIXED: Ab height 1920 aur width 1080 kar di hai (Full Screen 9:16)
    img_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1080&height=1920"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0"
    }
    
    time.sleep(10) # Pollinations API hit karne se pehle 10 second rukenge (Fixes 402 Error)
    
    try:
        response = requests.get(img_url, headers=headers, timeout=20)
        if response.status_code == 200:
            with open("reel_temp.jpg", "wb") as f:
                f.write(response.content)
            print("✅ Try 1 Success: AI Image Downloaded!")
            return
    except:
        pass

    print("⚠️ AI Blocked (402). Backup System Active: Downloading HQ Gaming Background...")
    # FIXED: Fallback images ko bhi vertical (1080x1920) size mein kar diya
    fallback_images = [
        "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=1080&h=1920&fit=crop", 
        "https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=1080&h=1920&fit=crop", 
        "https://images.unsplash.com/photo-1552820728-8b83bb6b7738?w=1080&h=1920&fit=crop", 
        "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=1080&h=1920&fit=crop"  
    ]
    try:
        r = requests.get(random.choice(fallback_images), timeout=20)
        if r.status_code == 200:
            with open("reel_temp.jpg", "wb") as f:
                f.write(r.content)
            print("✅ Try 2 Success: Backup Wallpaper Downloaded!")
            return
    except:
        pass

    print("⚠️ Wallpaper bhi fail. Solid background use kar rahe hain.")
    img = Image.new('RGB', (1080, 1920), color=(25, 25, 25))
    img.save('reel_temp.jpg')
    print("✅ Try 3 Success: Basic Background Ready!")

# 5. Video Banane ka Logic
def create_and_upload_reel():
    topic = get_topic()
    caption = f"POV: {topic} 💀😂\n\nYour Vote? 👇\n#EngineersGamer #GamingLife #Esports"
    
    print(f"🎨 Target Topic: {topic}")
    visual_prompt = get_safe_visual_prompt(topic)
    safe_prompt = urllib.parse.quote(visual_prompt)
    
    get_background_image(safe_prompt)
    
    img = Image.open("reel_temp.jpg")
    # FIXED: Ab image ko crop/resize karke proper 1080x1920 kiya hai, no borders!
    img = img.resize((1080, 1920), Image.Resampling.LANCZOS)
    img.save("reel_temp.jpg")

    print("🎬 Rendering 15s HD Reel...")
    
    # Ab bg_clip (kaala background) ki zaroorat nahi hai, kyu ki main image hi full screen hai
    img_clip = ImageClip("reel_temp.jpg").set_position('center').set_duration(15)
    
    wrapped_topic = textwrap.fill(topic.upper(), width=18) 
    
    topic_clip = TextClip(
        wrapped_topic, 
        fontsize=90,          
        color='white', 
        font='Arial-Bold', 
        align='center',
        stroke_color='black',
        stroke_width=6        
    ).set_position(('center', 380)).set_duration(15) 
    
    vote_clip = TextClip(
        "👇 COMMENT YOUR VOTE! 👇", 
        fontsize=70, 
        color='#FFD700', 
        font='Arial-Bold',
        align='center',
        stroke_color='black',
        stroke_width=4
    ).set_position(('center', 1450)).set_duration(15) 
    
    watermark = TextClip(
        "ER ASHU GAMING", 
        fontsize=45, 
        color='gray', 
        font='Arial-Bold'
    ).set_position(('center', 1750)).set_duration(15)
    
    # FIXED: bg_clip yahan se hata diya gaya hai
    video = CompositeVideoClip([img_clip, topic_clip, vote_clip, watermark])

    music_file = get_random_music()
    if music_file:
        audio = AudioFileClip(music_file).subclip(0, 15)
        video = video.set_audio(audio)

    video.write_videofile("final_reel.mp4", fps=24, codec='libx264', audio_codec='aac')

    page_id = '318640404662743'
    system_token = os.environ.get('FB_TOKEN')
    
    try:
        token_url = f"https://graph.facebook.com/{page_id}?fields=access_token&access_token={system_token}"
        token_response = requests.get(token_url).json()
        
        if 'access_token' in token_response:
            page_token = token_response['access_token']
        else:
            print(f"❌ Token Error: {token_response}")
            return

        url = f"https://graph-video.facebook.com/{page_id}/videos"
        with open("final_reel.mp4", 'rb') as video_file:
            files = {'source': video_file}
            payload = {'description': caption, 'title': 'Gaming Reels', 'access_token': page_token}
            
            print("🚀 Uploading to Facebook...")
            r = requests.post(url, data=payload, files=files)
            print(f"Upload Response: {r.json()}")
    except Exception as e:
        print(f"❌ Upload Error: {e}")

if __name__ == "__main__":
    create_and_upload_reel()

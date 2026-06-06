import requests
import os
import random
import json
import time
import urllib.parse
import textwrap
from PIL import Image
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip, AudioFileClip, ColorClip

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

def get_random_music():
    music_folder = "music"
    if os.path.exists(music_folder):
        files = [f for f in os.listdir(music_folder) if f.endswith(".mp3")]
        if files:
            return os.path.join(music_folder, random.choice(files))
    return None

# 🔥 MASTERSTROKE: Groq AI se Copyright naam hatwana
def get_safe_visual_prompt(topic):
    api_key = os.environ.get('GROQ_API_KEY')
    fallback_prompt = f"split screen gaming comparison, two warriors fighting, bright colors, 8k resolution"
    
    if not api_key: 
        return fallback_prompt

    try:
        prompt_instruction = (
            f"Create a short, vivid visual description for this gaming topic: '{topic}'. "
            "CRITICAL RULE: DO NOT use any copyrighted game names (like PUBG, Valorant, Free Fire) "
            "or specific character names (like Jett, Reyna, Alok). Use generic terms like 'wind ninja', "
            "'cyber soldier', 'vampire warrior', etc. Keep it under 15 words."
        )
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        data = {"model": "llama-3.1-8b-instant", "messages": [{"role": "user", "content": prompt_instruction}]}
        res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data, timeout=10)
        
        clean_desc = res.json()['choices'][0]['message']['content'].strip()
        clean_desc = clean_desc.replace('"', '').replace("'", "") # Remove any quotes
        return f"split screen comparison, {clean_desc}, epic gaming 3d render, 8k resolution"
    except Exception as e:
        print(f"Groq Sanitizer Error: {e}")
        return fallback_prompt

def create_and_upload_reel():
    topic = get_topic()
    caption = f"POV: {topic} 💀😂\n\nYour Vote? 👇\n#EngineersGamer #GamingLife #Esports"
    
    print(f"🎨 Target Topic: {topic}")
    
    # 🕵️ Yahan filter ho raha hai prompt
    visual_prompt = get_safe_visual_prompt(topic)
    print(f"🕵️ Copyright Bypass Prompt: {visual_prompt}")
    
    safe_prompt = urllib.parse.quote(visual_prompt)
    seed = int(time.time()) + random.randint(1, 1000)
    
    # Model explicitly 'flux' set kiya hai jo free aur fast hai
    img_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?seed={seed}&model=flux"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(img_url, headers=headers, timeout=60)
        
        if response.status_code == 200:
            with open("reel_temp.jpg", "wb") as f: 
                f.write(response.content)
                
            img = Image.open("reel_temp.jpg")
            img = img.resize((1080, 1080), Image.Resampling.LANCZOS)
            img.save("reel_temp.jpg")
            print("✅ Image successfully downloaded (Bypassed Copyright Filter)!")
        else:
            print(f"❌ Server ne Image nahi bheji. Status Code: {response.status_code}")
            return
            
    except Exception as e:
        print(f"❌ Image Download Error: {e}")
        return

    print("🎬 Rendering 15s HD Reel...")
    
    bg_clip = ColorClip(size=(1080, 1920), color=(15, 15, 15)).set_duration(15)
    img_clip = ImageClip("reel_temp.jpg").set_position('center').set_duration(15)
    
    wrapped_topic = textwrap.fill(topic.upper(), width=20)
    topic_clip = TextClip(
        wrapped_topic, 
        fontsize=75,
        color='white', 
        font='Arial-Bold', 
        align='center',
        stroke_color='black',
        stroke_width=3
    ).set_position(('center', 150)).set_duration(15)
    
    vote_clip = TextClip(
        "👇 COMMENT YOUR VOTE! 👇", 
        fontsize=70, 
        color='#FFD700', 
        font='Arial-Bold',
        align='center',
        stroke_color='black',
        stroke_width=3
    ).set_position(('center', 1550)).set_duration(15)
    
    watermark = TextClip(
        "ER ASHU GAMING", 
        fontsize=45, 
        color='gray', 
        font='Arial-Bold'
    ).set_position(('center', 1750)).set_duration(15)
    
    video = CompositeVideoClip([bg_clip, img_clip, topic_clip, vote_clip, watermark])

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

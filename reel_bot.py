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
        return "Building a Dirt House vs Digging a Cave"

def get_random_music():
    music_folder = "music"
    if os.path.exists(music_folder):
        files = [f for f in os.listdir(music_folder) if f.endswith(".mp3")]
        if files:
            return os.path.join(music_folder, random.choice(files))
    print("⚠️ Music folder ya files nahi mili.")
    return None

def create_and_upload_reel():
    topic = get_topic()
    caption = f"POV: {topic} 💀😂\n\nYour Vote? 👇\n#EngineersGamer #GamingLife #Esports"
    
    print(f"🎨 Image Generate ho rahi hai (COMPARISON STYLE): {topic}")
    seed = int(time.time()) + random.randint(1, 1000)
    
    visual_styles = [
        "split-screen comparison layout, two different gaming worlds side by side, 'choose your path' concept, a gamer standing in the middle deciding, vibrant 3D cartoonish style",
        "interactive social media poll format, horizontal split screen, bright and colorful gaming assets, stylized 3D render like Free Fire posters",
        "epic versus battle concept art, red vs blue neon lighting, divided screen, highly detailed 3D animated character style"
    ]
    random_style = random.choice(visual_styles)
    
    visual_prompt = f"Topic: {topic}. {random_style}, trending on facebook, bright colors, 8k resolution"
    safe_prompt = urllib.parse.quote(visual_prompt)
    
    # 1080x1080 (Square Image) taaki perfect center mein fit ho
    img_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1080&height=1080&seed={seed}&nologo=true"
    
    try:
        img_data = requests.get(img_url).content
        with open("reel_temp.jpg", "wb") as f: 
            f.write(img_data)
            
        img = Image.open("reel_temp.jpg")
        img = img.resize((1080, 1080), Image.Resampling.LANCZOS)
        img.save("reel_temp.jpg")
        
    except Exception as e:
        print(f"❌ Image Error: {e}")
        return

    print("🎬 Rendering 15s HD Reel...")
    
    # 🔥 FIX 1: Pitch Black Background (0, 0, 0)
    bg_clip = ColorClip(size=(1080, 1920), color=(0, 0, 0)).set_duration(15)
    
    # 🔥 FIX 2: Exact Center Image (Y-axis par 420 se 1500 tak jagah gheregi)
    img_clip = ImageClip("reel_temp.jpg").set_position('center').set_duration(15)
    
    # 🔥 FIX 3: Top Text (Bold, Pure White, No Stroke)
    # Width thodi kam ki hai (20 chars) taaki text naturally bada aur chouda dikhe
    wrapped_topic = textwrap.fill(topic, width=20)
    topic_clip = TextClip(
        wrapped_topic, 
        fontsize=85, # Size kaafi bada kar diya
        color='white', 
        font='Arial-Bold', 
        align='center'
    ).set_position(('center', 120)).set_duration(15) # Top black space ke center mein (Y=120)
    
    # 🔥 FIX 4: Bottom Text (Ekdum Meme jaisa bada text)
    vote_clip = TextClip(
        "COMMENT YOUR VOTE", 
        fontsize=80, 
        color='white', 
        font='Arial-Bold',
        align='center'
    ).set_position(('center', 1580)).set_duration(15) # Bottom black space mein (Y=1580)
    
    # WATERMARK (Thoda niche, thoda subtle)
    watermark = TextClip(
        "ER ASHU GAMING", 
        fontsize=35, 
        color='gray', 
        font='Arial-Bold'
    ).set_position(('center', 1800)).set_duration(15)
    
    video = CompositeVideoClip([bg_clip, img_clip, topic_clip, vote_clip, watermark])

    music_file = get_random_music()
    if music_file:
        audio = AudioFileClip(music_file).subclip(0, 15)
        video = video.set_audio(audio)

    video.write_videofile("final_reel.mp4", fps=24, codec='libx264', audio_codec='aac')

    # FACEBOOK UPLOAD
    page_id = '318640404662743'
    system_token = os.environ.get('FB_TOKEN')
    
    token_url = f"https://graph.facebook.com/{page_id}?fields=access_token&access_token={system_token}"
    token_response = requests.get(token_url).json()
    
    if 'access_token' in token_response:
        page_token = token_response['access_token']
    else:
        print(f"❌ Token Error: {token_response}")
        return

    url = f"https://graph-video.facebook.com/{page_id}/videos"
    
    try:
        with open("final_reel.mp4", 'rb') as video_file:
            files = {'source': video_file}
            payload = {
                'description': caption, 
                'title': 'Gaming Reels',
                'access_token': page_token
            }
            
            print("🚀 Uploading to Facebook...")
            r = requests.post(url, data=payload, files=files)
            print(f"Upload Response: {r.json()}")
    except Exception as e:
        print(f"❌ Upload Error: {e}")

if __name__ == "__main__":
    create_and_upload_reel()

import requests
import os
import random
import json
import time
import urllib.parse
import textwrap
from PIL import Image
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip, AudioFileClip

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
    print("⚠️ Music folder ya files nahi mili.")
    return None

def create_and_upload_reel():
    topic = get_topic()
    caption = f"POV: {topic} 💀😂\n\nYour Vote? 👇\n#EngineersGamer #GamingLife #Esports"
    
    print(f"🎨 Image Generate ho rahi hai (COMPARISON STYLE): {topic}")
    seed = int(time.time()) + random.randint(1, 1000)
    
    # 🔥 NAYA LOGIC: Engagement Bait / Split Screen Styles (1080x1920)
    visual_styles = [
        "split-screen comparison layout, two different gaming worlds side by side, 'choose your path' concept, a gamer standing in the middle deciding, vibrant 3D cartoonish style",
        "interactive social media poll format, 3-way horizontal split screen, bright and colorful gaming assets, stylized 3D render like Free Fire posters",
        "epic versus battle concept art, red vs blue neon lighting, divided screen, highly detailed 3D animated character style",
        "grid layout showing different glowing gaming items, 'which one are you using' concept, vivid colors, masterpiece"
    ]
    random_style = random.choice(visual_styles)
    
    # Prompt ko merge karna
    visual_prompt = f"Topic: {topic}. {random_style}, trending on facebook, bright colors, 8k resolution"
    safe_prompt = urllib.parse.quote(visual_prompt)
    
    # EXACT Reel Size (1080x1920) set kiya hai taaki full screen aaye
    img_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1080&height=1920&seed={seed}&nologo=true"
    
    try:
        img_data = requests.get(img_url).content
        with open("reel_temp.jpg", "wb") as f: 
            f.write(img_data)
            
        # Image ko bina stretch kiye exactly screen par fit karna
        img = Image.open("reel_temp.jpg")
        img = img.resize((1080, 1920), Image.Resampling.LANCZOS)
        img.save("reel_temp.jpg")
        
    except Exception as e:
        print(f"❌ Image Error: {e}")
        return

    print("🎬 Rendering 15s HD Reel...")
    
    # OVERLAY LAYOUT DESIGN
    img_clip = ImageClip("reel_temp.jpg").set_duration(15)
    
    # TOP TEXT
    wrapped_topic = textwrap.fill(topic, width=22)
    topic_clip = TextClip(
        wrapped_topic, 
        fontsize=70,
        color='white', 
        font='Arial-Bold', 
        align='center',
        stroke_color='black',
        stroke_width=4
    ).set_position(('center', 200)).set_duration(15)
    
    # BOTTOM TEXT 
    vote_clip = TextClip(
        "👇 COMMENT YOUR VOTE!", 
        fontsize=65, 
        color='#FFD700', 
        font='Arial-Bold',
        align='center',
        stroke_color='black',
        stroke_width=4
    ).set_position(('center', 1500)).set_duration(15)
    
    # WATERMARK
    watermark = TextClip(
        "Er Ashu Gaming", 
        fontsize=40, 
        color='white', 
        font='Arial-Bold',
        stroke_color='black',
        stroke_width=2
    ).set_position(('center', 1720)).set_duration(15)
    
    video = CompositeVideoClip([img_clip, topic_clip, vote_clip, watermark])

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

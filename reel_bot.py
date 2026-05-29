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
        return "Free Fire vs BGMI: Asli King kaun?"

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
    caption = f"POV: {topic} 💀😂\n\nComment below! 👇\n#EngineersGamer #GamingLife #ReelsIndia"
    
    # 1. FULL SCREEN IMAGE GENERATION (1080x1920)
    print(f"🎨 Image Generate ho rahi hai: {topic}")
    seed = int(time.time())
    visual_prompt = f"{topic}, ultra-realistic gaming environment, photorealistic, Unreal Engine 5 render, cinematic lighting, 8k resolution, dark and gritty tone"
    safe_prompt = urllib.parse.quote(visual_prompt)
    img_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1080&height=1920&seed={seed}&nologo=true"
    
    try:
        img_data = requests.get(img_url).content
        with open("reel_temp.jpg", "wb") as f: 
            f.write(img_data)
            
        # Image ko exact Screen Size par set karna taaki stretch na ho aur gap na bache
        img = Image.open("reel_temp.jpg")
        img = img.resize((1080, 1920), Image.Resampling.LANCZOS)
        img.save("reel_temp.jpg")
        
    except Exception as e:
        print(f"❌ Image Error: {e}")
        return

    print("🎬 Rendering 15s HD Reel...")
    
    # 2. OVERLAY LAYOUT DESIGN
    # Layer 1: Full Screen Image
    img_clip = ImageClip("reel_temp.jpg").set_duration(15)
    
    # Layer 2: TOP TEXT (Image ke upar, Black Stroke ke sath taaki clear dikhe)
    wrapped_topic = textwrap.fill(topic, width=22)
    topic_clip = TextClip(
        wrapped_topic, 
        fontsize=75,
        color='white', 
        font='Arial-Bold', 
        align='center',
        stroke_color='black',  # NAYA: Text readable banane ke liye outline
        stroke_width=4
    ).set_position(('center', 250)).set_duration(15)
    
    # Layer 3: BOTTOM TEXT (Image ke niche wale hisse par)
    vote_clip = TextClip(
        "👇 COMMENT YOUR VOTE!", 
        fontsize=60, 
        color='#FFD700', 
        font='Arial-Bold',
        align='center',
        stroke_color='black',
        stroke_width=4
    ).set_position(('center', 1550)).set_duration(15)
    
    # Layer 4: WATERMARK
    watermark = TextClip(
        "Er Ashu Gaming", 
        fontsize=40, 
        color='white', 
        font='Arial-Bold',
        stroke_color='black',
        stroke_width=2
    ).set_position(('center', 1720)).set_duration(15)
    
    # Sabhi layers ko ek ke upar ek rakh diya
    video = CompositeVideoClip([img_clip, topic_clip, vote_clip, watermark])

    music_file = get_random_music()
    if music_file:
        audio = AudioFileClip(music_file).subclip(0, 15)
        video = video.set_audio(audio)

    video.write_videofile("final_reel.mp4", fps=24, codec='libx264', audio_codec='aac')

    # 3. FACEBOOK UPLOAD
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

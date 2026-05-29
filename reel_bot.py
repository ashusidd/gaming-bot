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
    
    print(f"🎨 Image Generate ho rahi hai: {topic}")
    seed = int(time.time())
    visual_prompt = f"{topic}, 3D high quality gaming concept art, highly detailed, vivid colors"
    safe_prompt = urllib.parse.quote(visual_prompt)
    img_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1080&height=1920&seed={seed}&nologo=true"
    
    try:
        img_data = requests.get(img_url).content
        with open("reel_temp.jpg", "wb") as f: 
            f.write(img_data)
            
        # FIX 1: Image Stretching Fix (PIL use karke perfect 9:16 Crop & Resize)
        img = Image.open("reel_temp.jpg")
        target_ratio = 1080 / 1920
        img_ratio = img.width / img.height
        
        if img_ratio > target_ratio:
            new_width = int(target_ratio * img.height)
            offset = (img.width - new_width) // 2
            img = img.crop((offset, 0, img.width - offset, img.height))
        else:
            new_height = int(img.width / target_ratio)
            offset = (img.height - new_height) // 2
            img = img.crop((0, offset, img.width, img.height - offset))
            
        img = img.resize((1080, 1920), Image.Resampling.LANCZOS)
        img.save("reel_temp_fixed.jpg")
        
    except Exception as e:
        print(f"❌ Image Error: {e}")
        return

    print("🎬 Rendering 15s HD Reel...")
    clip = ImageClip("reel_temp_fixed.jpg").set_duration(15)
    
    # FIX 2: Text Overflow Fix (Manual Wrap at 22 characters)
    wrapped_topic = textwrap.fill(topic, width=22)
    final_text = f"{wrapped_topic}\n\n👇 COMMENT YOUR VOTE!"
    
    txt = TextClip(
        final_text, 
        fontsize=65, 
        color='white', 
        font='Arial-Bold', 
        align='center', 
        stroke_color='black', 
        stroke_width=3
    ).set_pos('center').set_duration(15)
    
    # FIX 3: Watermark Visibility Fix (Position 1500)
    watermark = TextClip(
        "Er Ashu Gaming", 
        fontsize=45, 
        color='white', 
        font='Arial-Bold', 
        stroke_color='black', 
        stroke_width=2
    ).set_pos(('center', 1500)).set_duration(15)
    
    video = CompositeVideoClip([clip, txt, watermark])

    music_file = get_random_music()
    if music_file:
        audio = AudioFileClip(music_file).subclip(0, 15)
        video = video.set_audio(audio)

    video.write_videofile("final_reel.mp4", fps=24, codec='libx264', audio_codec='aac')

    # Facebook Upload
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
            # FIX 4: FB Video Caption Fix (message ki jagah description)
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

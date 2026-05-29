import requests
import os
import random
import json
import time
import urllib.parse
import textwrap
from PIL import Image  # NAYA: Image ko exact 1080px fit karne ke liye
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
    img_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1080&height=1080&seed={seed}&nologo=true"
    
    try:
        img_data = requests.get(img_url).content
        with open("reel_temp.jpg", "wb") as f: 
            f.write(img_data)
            
        # THE FIX: Image ko zabardasti 1080x1080 karna taaki side gap na bache
        img = Image.open("reel_temp.jpg")
        img = img.resize((1080, 1080), Image.Resampling.LANCZOS)
        img.save("reel_temp.jpg")
        
    except Exception as e:
        print(f"❌ Image Error: {e}")
        return

    print("🎬 Rendering 15s HD Reel...")
    
    # Background (Dark Grey)
    bg_clip = ColorClip(size=(1080, 1920), color=(15, 15, 15)).set_duration(15)
    
    # Square Image (Ab yeh poori width cover karegi)
    img_clip = ImageClip("reel_temp.jpg").set_position('center').set_duration(15)
    
    # TOP TEXT
    wrapped_topic = textwrap.fill(topic, width=25)
    topic_clip = TextClip(
        wrapped_topic, 
        fontsize=75,
        color='white', 
        font='Arial-Bold', 
        align='center'
    ).set_position(('center', 180)).set_duration(15)
    
    # BOTTOM TEXT 
    vote_clip = TextClip(
        "👇 COMMENT YOUR VOTE!", 
        fontsize=60, 
        color='#FFD700', 
        font='Arial-Bold',
        align='center'
    ).set_position(('center', 1550)).set_duration(15)
    
    # WATERMARK
    watermark = TextClip(
        "Er Ashu Gaming", 
        fontsize=40, 
        color='white', 
        font='Arial-Bold'
    ).set_position(('center', 1720)).set_duration(15)
    
    # Layers merge
    video = CompositeVideoClip([bg_clip, img_clip, topic_clip, vote_clip, watermark])

    music_file = get_random_music()
    if music_file:
        audio = AudioFileClip(music_file).subclip(0, 15)
        video = video.set_audio(audio)

    video.write_videofile("final_reel.mp4", fps=24, codec='libx264', audio_codec='aac')

    # Facebook Upload Logic
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

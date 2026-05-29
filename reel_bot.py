import requests
import os
import random
import json
import time
import urllib.parse
import textwrap
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
    
    # 1. SQUARE IMAGE GENERATE KARNA (1080x1080) - Stretch nahi hogi
    print(f"🎨 Image Generate ho rahi hai: {topic}")
    seed = int(time.time())
    visual_prompt = f"{topic}, 3D high quality gaming concept art, highly detailed, vivid colors"
    safe_prompt = urllib.parse.quote(visual_prompt)
    img_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1080&height=1080&seed={seed}&nologo=true"
    
    try:
        img_data = requests.get(img_url).content
        with open("reel_temp.jpg", "wb") as f: 
            f.write(img_data)
    except Exception as e:
        print(f"❌ Image Error: {e}")
        return

    print("🎬 Rendering 15s HD Reel...")
    
    # 2. UI LAYOUT DESIGN (Frontend Style)
    # Layer 1: Dark Grey Background (1080x1920)
    bg_clip = ColorClip(size=(1080, 1920), color=(20, 20, 20)).set_duration(15)
    
    # Layer 2: Square Image (Center mein placed)
    img_clip = ImageClip("reel_temp.jpg").set_position('center').set_duration(15)
    
    # Layer 3: Main Text (Upar ki taraf - Y position 250)
    wrapped_topic = textwrap.fill(topic, width=25)
    final_text = f"{wrapped_topic}\n\n👇 COMMENT YOUR VOTE!"
    txt_clip = TextClip(
        final_text, 
        fontsize=65, 
        color='white', 
        font='Arial-Bold', 
        align='center'
    ).set_position(('center', 250)).set_duration(15)
    
    # Layer 4: Watermark (Niche ki taraf - Y position 1550)
    watermark = TextClip(
        "Er Ashu Gaming", 
        fontsize=45, 
        color='#FFD700',  # Thoda golden/yellow color diya hai taaki alag se chamke
        font='Arial-Bold'
    ).set_position(('center', 1550)).set_duration(15)
    
    # Sabhi layers ko ek ke upar ek rakh diya
    video = CompositeVideoClip([bg_clip, img_clip, txt_clip, watermark])

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
            # FACEBOOK CAPTION FIX: Video ke liye 'description' use hota hai
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

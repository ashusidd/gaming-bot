import sys
import subprocess
import os
import json
import random
import time
import textwrap
import requests

# --- AUTO-INSTALLER (Dependecy error nahi aayega) ---
def install(package):
    print(f"Installing {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    from PIL import Image
    from moviepy.editor import ImageClip, TextClip, CompositeVideoClip, AudioFileClip, ColorClip
except ImportError:
    install("pillow")
    install("moviepy")
    from PIL import Image
    from moviepy.editor import ImageClip, TextClip, CompositeVideoClip, AudioFileClip, ColorClip

# --- BOT LOGIC ---
def get_topic():
    try:
        with open("topics.json", "r+") as f:
            data = json.load(f)
            remaining = [t for t in data["all_topics"] if t not in data.get("used_topics", [])]
            if not remaining:
                data["used_topics"] = []
                remaining = data["all_topics"]
            topic = random.choice(remaining)
            data["used_topics"] = data.get("used_topics", []) + [topic]
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
            return topic
    except:
        return "Pro Gaming Moments"

def get_random_music():
    music_folder = "music"
    if os.path.exists(music_folder):
        files = [f for f in os.listdir(music_folder) if f.endswith(".mp3")]
        if files: return os.path.join(music_folder, random.choice(files))
    return None

def generate_image(prompt):
    print(f"🚀 Generating AI Image for: {prompt}")
    safe_prompt = prompt.replace(" ", "%20")
    # Pollinations AI: Fast, Free, No Token Needed
    url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1080&height=1080&seed={random.randint(1,9999)}"
    try:
        response = requests.get(url, timeout=60)
        if response.status_code == 200:
            with open("reel_temp.jpg", "wb") as f: f.write(response.content)
            return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_and_upload_reel():
    topic = get_topic()
    caption = f"POV: {topic} 💀😂\n\nYour Vote? 👇\n#ErAshuGaming #GamingLife"
    
    if not generate_image(topic): return

    print("🎬 Rendering Reel...")
    bg = ColorClip(size=(1080, 1920), color=(0, 0, 0)).set_duration(15)
    img = ImageClip("reel_temp.jpg").set_position('center').set_duration(15)
    
    txt = TextClip(textwrap.fill(topic.upper(), 20), fontsize=85, color='white', font='Arial-Bold', align='center').set_position(('center', 150)).set_duration(15)
    wm = TextClip("ER ASHU GAMING", fontsize=40, color='gray').set_position(('center', 1800)).set_duration(15)
    
    video = CompositeVideoClip([bg, img, txt, wm])
    
    music = get_random_music()
    if music:
        audio = AudioFileClip(music).subclip(0, 15)
        video = video.set_audio(audio)

    video.write_videofile("final_reel.mp4", fps=24, codec='libx264', audio_codec='aac')

    # Upload
    page_id = '318640404662743'
    token = os.environ.get('FB_TOKEN')
    with open("final_reel.mp4", 'rb') as f:
        r = requests.post(f"https://graph-video.facebook.com/{page_id}/videos", 
                          data={'description': caption, 'access_token': token}, files={'source': f})
        print(f"✅ Response: {r.json()}")

if __name__ == "__main__":
    create_and_upload_reel()

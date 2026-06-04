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
            f.seek(0); json.dump(data, f, indent=4); f.truncate()
        return topic
    except Exception as e:
        print(f"Topic Error: {e}")
        return "M762 Beryl vs AKM"

def get_random_music():
    music_folder = "music"
    if os.path.exists(music_folder) and os.listdir(music_folder):
        files = [f for f in os.listdir(music_folder) if f.endswith(".mp3")]
        if files: return os.path.join(music_folder, random.choice(files))
    return None

def generate_pure_ai_image(prompt):
    encoded_prompt = urllib.parse.quote(prompt)
    # 🔥 NEW ENDPOINT: Yeh completely free hai aur bina rate limit ke chalta hai
    API_URL = f"https://v1.ai.pollinations.ai/p/{encoded_prompt}?width=1080&height=1080&model=searchglow"
    
    max_retries = 3
    for attempt in range(max_retries):
        print(f"Free API se image nikal rahe hain (Attempt {attempt + 1}/3)...")
        try:
            response = requests.get(API_URL, timeout=30)
            if response.status_code == 200:
                with open("reel_temp.jpg", "wb") as f:
                    f.write(response.content)
                print("✅ Pure AI Image successfully generated!")
                return True
            else:
                print(f"⚠️ Status Code: {response.status_code}. Retrying...")
                time.sleep(5)
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(5)
    return False

def create_and_upload_reel():
    topic = get_topic()
    caption = f"POV: {topic} 💀😂\n\nYour Vote? 👇\n#EngineersGamer #GamingLife #Esports"
    
    if not generate_pure_ai_image(f"{topic}, dynamic gaming action 3d render, vibrant style, 4k"):
        print("🛑 UPLOAD CANCELLED: AI Image nahi bani. No Fallback rule.")
        return

    bg_clip = ColorClip(size=(1080, 1920), color=(0, 0, 0)).set_duration(15)
    img_clip = ImageClip("reel_temp.jpg").set_position('center').set_duration(15)
    
    wrapped_topic = textwrap.fill(topic.upper(), width=20)
    topic_clip = TextClip(wrapped_topic, fontsize=85, color='white', font='Arial-Bold', align='center').set_position(('center', 120)).set_duration(15) 
    vote_clip = TextClip("COMMENT YOUR VOTE", fontsize=80, color='white', font='Arial-Bold', align='center').set_position(('center', 1580)).set_duration(15) 
    watermark = TextClip("ER ASHU GAMING", fontsize=35, color='gray', font='Arial-Bold').set_position(('center', 1800)).set_duration(15)
    
    video = CompositeVideoClip([bg_clip, img_clip, topic_clip, vote_clip, watermark])

    music_file = get_random_music()
    if music_file:
        audio = AudioFileClip(music_file).subclip(0, 15)
        video = video.set_audio(audio)

    video.write_videofile("final_reel.mp4", fps=24, codec='libx264', audio_codec='aac')

    page_id = '318640404662743'
    system_token = os.environ.get('FB_TOKEN')
    try:
        page_token = requests.get(f"https://graph.facebook.com/{page_id}?fields=access_token&access_token={system_token}").json().get('access_token')
        if page_token:
            with open("final_reel.mp4", 'rb') as video_file:
                r = requests.post(f"https://graph-video.facebook.com/{page_id}/videos", data={'description': caption, 'title': 'Gaming Reels', 'access_token': page_token}, files={'source': video_file})
                print(f"Facebook Response: {r.json()}")
    except Exception as e:
        print(f"❌ Upload Error: {e}")

if __name__ == "__main__":
    create_and_upload_reel()
    

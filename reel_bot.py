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
        return "Flying an Oppressor Mk II vs Driving a Supercar: GTA Online?"

def get_random_music():
    music_folder = "music"
    if os.path.exists(music_folder):
        files = [f for f in os.listdir(music_folder) if f.endswith(".mp3")]
        if files:
            return os.path.join(music_folder, random.choice(files))
    print("⚠️ Music folder ya files nahi mili.")
    return None

def generate_pure_ai_image(prompt):
    encoded_prompt = urllib.parse.quote(prompt)
    # 🔥 LIGHTWEIGHT TURBO ENGINE: Is endpoint par 402/payment errors nahi aate hain
    API_URL = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1080&nologo=true"
    
    max_retries = 3
    for attempt in range(max_retries):
        unique_seed = int(time.time()) + random.randint(1, 1000)
        seeded_url = f"{API_URL}&seed={unique_seed}"
        
        print(f"Pollinations AI (Turbo Engine) se image nikal rahe hain (Attempt {attempt + 1}/3)...")
        try:
            response = requests.get(seeded_url, timeout=30)
            if response.status_code == 200 and 'image' in response.headers.get('Content-Type', ''):
                with open("reel_temp.jpg", "wb") as f:
                    f.write(response.content)
                
                # Image ko verify aur resize karne ke liye
                img = Image.open("reel_temp.jpg")
                img = img.resize((1080, 1080), Image.Resampling.LANCZOS)
                img.save("reel_temp.jpg")
                
                print("✅ Premium AI Image successfully generated!")
                return True
            else:
                print(f"⚠️ Server Response: {response.status_code}. Retrying in 5s...")
                time.sleep(5)
        except Exception as e:
            print(f"❌ Network issue on attempt {attempt + 1}: {e}")
            time.sleep(5)
    return False

def create_and_upload_reel():
    topic = get_topic()
    caption = f"POV: {topic} 💀😂\n\nYour Vote? 👇\n#EngineersGamer #GamingLife #Esports"
    
    print(f"🎨 Target Topic: {topic}")
    
    # STRICTION: Agar AI image nahi bani, toh seedha cancel, koi fallback nahi!
    visual_prompt = f"{topic}, split-screen comparison layout, dynamic two different gaming sides, bright cinematic lighting, 3d rendering style, masterpiece"
    if not generate_pure_ai_image(visual_prompt):
        print("🛑 UPLOAD CANCELLED: Pure AI Image nahi ban payi. Strict Rule enforced.")
        return

    print("🎬 Rendering 15s HD Reel...")
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

    # FACEBOOK UPLOAD
    page_id = '318640404662743'
    system_token = os.environ.get('FB_TOKEN')
    
    token_url = f"https://graph.facebook.com/{page_id}?fields=access_token&access_token={system_token}"
    try:
        token_response = requests.get(token_url).json()
        if 'access_token' in token_response:
            page_token = token_response['access_token']
        else:
            print(f"❌ Token Error: {token_response}")
            return
            
        url = f"https://graph-video.facebook.com/{page_id}/videos"
        with open("final_reel.mp4", 'rb') as video_file:
            files = {'source': video_file}
            payload = {
                'description': caption, 
                'title': 'Gaming Reels',
                'access_token': page_token
            }
            print("🚀 Uploading Reel to Facebook...")
            r = requests.post(url, data=payload, files=files)
            print(f"Upload Response: {r.json()}")
    except Exception as e:
        print(f"❌ Upload Error: {e}")

if __name__ == "__main__":
    create_and_upload_reel()
    

import os
import json
import random
import time
import textwrap
import requests
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
        return "Aggressive Rusher vs Tactical Camper: Your playstyle?"

def get_random_music():
    music_folder = "music"
    if os.path.exists(music_folder) and os.listdir(music_folder):
        files = [f for f in os.listdir(music_folder) if f.endswith(".mp3")]
        if files: return os.path.join(music_folder, random.choice(files))
    return None

def generate_pure_ai_image(prompt):
    token = os.environ.get('HF_TOKEN')
    if not token:
        print("❌ ERROR: HF_TOKEN GitHub secrets mein nahi mila!")
        return False

    # Sabse stable aur fast model use kar rahe hain
    API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    headers = {"Authorization": f"Bearer {token}"}
    
    realistic_prompt = f"masterpiece, highly detailed, {prompt}, ultra-realistic 3D gaming render, cinematic lighting, 4k"
    
    # 5 attempts ka loop, taaki server wakeup time handle ho sake
    for attempt in range(5):
        print(f"🚀 Direct API (Hugging Face) se image nikal rahe hain (Attempt {attempt + 1}/5)...")
        try:
            response = requests.post(API_URL, headers=headers, json={"inputs": realistic_prompt}, timeout=60)
            
            if response.status_code == 200:
                with open("reel_temp.jpg", "wb") as f:
                    f.write(response.content)
                
                img = Image.open("reel_temp.jpg")
                img = img.resize((1080, 1080), Image.Resampling.LANCZOS)
                img.save("reel_temp.jpg")
                
                print("✅ Direct API se Ultra-HD AI Image ban gayi!")
                return True
            
            elif response.status_code == 503:
                # Agar model sleep mode mein hai, toh API khud batati hai kitna wait karna hai
                error_data = response.json()
                wait_time = error_data.get('estimated_time', 20)
                print(f"⏳ AI Model load ho raha hai. {wait_time} seconds wait kar rahe hain...")
                time.sleep(wait_time + 2) # Thoda extra buffer
            else:
                print(f"❌ API Error {response.status_code}: {response.text}")
                time.sleep(10)
                
        except Exception as e:
            print(f"❌ Connection Error: {e}")
            time.sleep(10)
            
    return False

def create_and_upload_reel():
    topic = get_topic()
    caption = f"POV: {topic} 💀😂\n\nYour Vote? 👇\n#EngineersGamer #GamingLife #Esports"
    
    print(f"🎨 Target Topic: {topic}")
    
    if not generate_pure_ai_image(topic):
        print("🛑 UPLOAD CANCELLED: AI Image nahi bani. Strict Rule enforced.")
        return

    print("🎬 Rendering 15s HD Reel using MoviePy...")
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
            print("🚀 Uploading Reel to Facebook...")
            with open("final_reel.mp4", 'rb') as video_file:
                r = requests.post(f"https://graph-video.facebook.com/{page_id}/videos", data={'description': caption, 'title': 'Gaming Reels', 'access_token': page_token}, files={'source': video_file})
                print(f"Facebook Response: {r.json()}")
    except Exception as e:
        print(f"❌ Upload Error: {e}")

if __name__ == "__main__":
    create_and_upload_reel()

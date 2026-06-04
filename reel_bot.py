import os
import json
import random
import time
import textwrap
import requests
from PIL import Image
from huggingface_hub import InferenceClient
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
        print("❌ ERROR: HF_TOKEN nahi mila!")
        return False

    client = InferenceClient(provider="hf-inference", token=token)
    
    # 'mdjrny-v4 style' lagane se openjourney model ekdum cinematic output deta hai
    realistic_prompt = f"mdjrny-v4 style, {prompt}, ultra-realistic 3D gaming render, cinematic lighting, masterpiece, 4k"
    
    max_retries = 3
    delay = 20 # Shuruwaati break
    
    for attempt in range(max_retries):
        print(f"Hugging Face SDK Client se image nikal rahe hain (Attempt {attempt + 1}/3)...")
        try:
            image = client.text_to_image(
                prompt=realistic_prompt,
                # 🔥 Light aur super fast model jo kam rate-limit hota hai
                model="prompthero/openjourney"
            )
            image.save("reel_temp.jpg")
            
            img = Image.open("reel_temp.jpg")
            img = img.resize((1080, 1080), Image.Resampling.LANCZOS)
            img.save("reel_temp.jpg")
            
            print("✅ Pure Realistic AI Image successfully generated!")
            return True
        except Exception as e:
            print(f"❌ Error on attempt {attempt + 1}: {e}")
            if "429" in str(e):
                print(f"⏳ Server busy (429)! {delay} seconds ka smart break le rahe hain...")
                time.sleep(delay)
                delay = delay * 2 # Agli baar delay double ho jayega
            else:
                time.sleep(5)
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
    

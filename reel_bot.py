import requests
import os
import random
import json
import time
import urllib.parse
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip, AudioFileClip

def get_topic():
    try:
        with open("topics.json", "r+") as f:
            data = json.load(f)
            remaining = [t for t in data["all_topics"] if t not in data["used_topics"]]
            if not remaining:
                # Agar saare topics use ho gaye, toh list reset kar do
                data["used_topics"] = []
                remaining = data["all_topics"]
            topic = random.choice(remaining)
            data["used_topics"].append(topic)
            f.seek(0)
            json.dump(data, f, indent=4)
            # Purana bacha hua data truncate karna (taaki file corrupt na ho)
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
    print("⚠️ Music file nahi mili. Bina gaane ke Reel banegi.")
    return None

def create_and_upload_reel():
    topic = get_topic()
    caption = f"POV: {topic} 💀😂\n\nComment below! 👇\n#EngineersGamer #GamingLife #ReelsIndia"
    
    # 1. Download Image (Visual prompt enhance kiya gaya hai)
    print(f"🎨 Image Generate ho rahi hai topic par: {topic}")
    seed = int(time.time())
    visual_prompt = f"{topic}, 3D high quality gaming concept art, highly detailed, vivid colors"
    safe_prompt = urllib.parse.quote(visual_prompt)
    img_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1080&height=1920&seed={seed}&nologo=true"
    
    try:
        img_data = requests.get(img_url).content
        with open("reel_temp.jpg", "wb") as f: 
            f.write(img_data)
    except Exception as e:
        print(f"❌ Image Download Error: {e}")
        return

    # 2. Render Video (15 Seconds)
    print("🎬 Rendering 15s Reel...")
    clip = ImageClip("reel_temp.jpg").set_duration(15)
    
    # TextClip (ImageMagick ab allow karega)
    txt = TextClip(f"{topic}\nCOMMENT YOUR VOTE!", fontsize=50, color='white', font='Arial-Bold', size=(800, None), method='caption').set_pos('center').set_duration(15)
    video = CompositeVideoClip([clip, txt])

    music_file = get_random_music()
    if music_file:
        # Fadeout hata diya gaya hai taaki error na aaye
        audio = AudioFileClip(music_file).subclip(0, 15)
        video = video.set_audio(audio)

    video.write_videofile("final_reel.mp4", fps=24, codec='libx264', audio_codec='aac')

    # 3. Upload with PAGE TOKEN
    page_id = '318640404662743'
    system_token = os.environ.get('FB_TOKEN')
    
    token_url = f"https://graph.facebook.com/{page_id}?fields=access_token&access_token={system_token}"
    token_response = requests.get(token_url).json()
    
    if 'access_token' in token_response:
        page_token = token_response['access_token']
        print("✅ Success: Page Access Token mil gaya!")
    else:
        print(f"❌ Token Error: {token_response}")
        return

    url = f"https://graph-video.facebook.com/{page_id}/videos"
    
    try:
        with open("final_reel.mp4", 'rb') as video_file:
            files = {'source': video_file}
            payload = {'message': caption, 'access_token': page_token}
            
            print("🚀 Facebook par Reel upload ho rahi hai...")
            r = requests.post(url, data=payload, files=files)
            print(f"Upload Response: {r.json()}")
    except Exception as e:
        print(f"❌ Upload Error: {e}")

if __name__ == "__main__":
    create_and_upload_reel()

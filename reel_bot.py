import requests, os, random, json, time
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip, AudioFileClip

def get_topic():
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
    return topic

def get_random_music():
    music_folder = "music"
    files = [f for f in os.listdir(music_folder) if f.endswith(".mp3")]
    return os.path.join(music_folder, random.choice(files)) if files else None

def create_and_upload_reel():
    topic = get_topic()
    caption = f"POV: {topic} 💀😂\n\nComment below! 👇\n#EngineersGamer #GamingLife #ReelsIndia"
    
    # 1. Download Image
    seed = int(time.time())
    img_url = f"https://image.pollinations.ai/prompt/{topic}?width=1080&height=1920&seed={seed}"
    img_data = requests.get(img_url).content
    with open("reel_temp.jpg", "wb") as f: f.write(img_data)

    # 2. Render Video (15 Seconds)
    print("🎬 Rendering 15s Reel...")
    clip = ImageClip("reel_temp.jpg").set_duration(15)
    txt = TextClip(f"{topic}\nCOMMENT YOUR VOTE!", fontsize=50, color='white', font='Arial-Bold', size=(800, None), method='caption').set_pos('center').set_duration(15)
    video = CompositeVideoClip([clip, txt])

    music_file = get_random_music()
    if music_file:
        audio = AudioFileClip(music_file).subclip(0, 15)
        video = video.set_audio(audio)

    video.write_videofile("final_reel.mp4", fps=24, codec='libx264', audio_codec='aac')

    # 3. Upload
    page_id = '318640404662743'
    token = os.environ.get('FB_TOKEN')
    url = f"https://graph-video.facebook.com/{page_id}/videos"
    files = {'source': open("final_reel.mp4", 'rb')}
    payload = {'message': caption, 'access_token': token}
    r = requests.post(url, data=payload, files=files)
    print(f"Upload Response: {r.json()}")

if __name__ == "__main__":
    create_and_upload_reel()

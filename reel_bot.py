import os
import json
import random
import textwrap
import requests
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip, ColorClip

def get_topic():
    with open("topics.json", "r") as f:
        data = json.load(f)
        return random.choice(data["all_topics"])

def generate_image(prompt):
    print(f"🚀 AI Image bana raha hoon: {prompt}")
    safe_prompt = prompt.replace(" ", "%20")
    url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1080&height=1920&nologo=true&seed={random.randint(1,9999)}"
    try:
        response = requests.get(url, timeout=60)
        with open("reel_temp.jpg", "wb") as f: 
            f.write(response.content)
        return True
    except:
        return False

def create_and_upload_reel():
    topic = get_topic()
    if not generate_image(topic): 
        print("❌ Image nahi bani!")
        return

    print("🎬 MoviePy se Reel render kar raha hoon...")
    bg = ColorClip(size=(1080, 1920), color=(0, 0, 0)).set_duration(15)
    img = ImageClip("reel_temp.jpg").set_position('center').set_duration(15)
    
    txt = TextClip(textwrap.fill(topic.upper(), 20), fontsize=85, color='white', font='Arial-Bold', align='center').set_position(('center', 150)).set_duration(15)
    wm = TextClip("ER ASHU GAMING", fontsize=45, color='gray').set_position(('center', 1800)).set_duration(15)
    
    video = CompositeVideoClip([bg, img, txt, wm])
    video.write_videofile("final_reel.mp4", fps=24, codec='libx264', audio_codec='aac')

    token = os.environ.get('FB_TOKEN')
    page_id = '318640404662743'
    caption = f"POV: {topic} 🔥\n\n#ErAshuGaming #GamingLife #Esports"
    
    with open("final_reel.mp4", 'rb') as f:
        requests.post(f"https://graph-video.facebook.com/{page_id}/videos", 
                      data={'description': caption, 'access_token': token}, files={'source': f})
    print("✅ Reel Posted!")

if __name__ == "__main__":
    create_and_upload_reel()

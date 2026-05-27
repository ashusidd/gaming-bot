import datetime
import subprocess
import os

def run():
    now = datetime.datetime.utcnow()
    # 2 PM IST = 08:30 UTC, 9 PM IST = 15:30 UTC
    # Hum 15 minute ka window le rahe hain taaki agar GitHub thoda late chale toh bhi run ho
    if (now.hour == 8 and 30 <= now.minute < 45) or (now.hour == 15 and 30 <= now.minute < 45):
        print("Mode: REEL")
        subprocess.run(["python", "reel_bot.py"])
    else:
        print("Mode: PHOTO")
        subprocess.run(["python", "final_bot.py"])

if __name__ == "__main__":
    run()

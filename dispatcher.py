import subprocess
import datetime

def run():
    # Server ka current time (UTC format) nikal rahe hain
    now = datetime.datetime.utcnow()
    
    # 2 PM IST = 08:30 UTC, 9 PM IST = 15:30 UTC
    # Agar time match hota hai, toh Reel banegi
    if (now.hour == 8 and 30 <= now.minute < 45) or (now.hour == 15 and 30 <= now.minute < 45):
        print("Mode: REEL")
        subprocess.run(["python", "reel_bot.py"])
        
    # Baaki kisi bhi time par GitHub action chalega toh Photo banegi
    else:
        print("Mode: PHOTO")
        subprocess.run(["python", "final_bot.py"])

if __name__ == "__main__":
    run()

import subprocess
import datetime

def run():
    # TEST MODE: Zabardasti Reel chala rahe hain taaki live test ho sake
    print("🚀 Testing Mode: Forcing REEL Bot execution...")
    subprocess.run(["python", "reel_bot.py"])

    # --- JAB REEL POST HO JAYE, TOH NICHE WALE CODE KO UNCOMMENT (CHALU) KAR DENA ---
    # now = datetime.datetime.utcnow()
    # # 2 PM IST = 08:30 UTC, 9 PM IST = 15:30 UTC
    # if (now.hour == 8 and 30 <= now.minute < 45) or (now.hour == 15 and 30 <= now.minute < 45):
    #     print("Mode: REEL")
    #     subprocess.run(["python", "reel_bot.py"])
    # else:
    #     print("Mode: PHOTO")
    #     subprocess.run(["python", "final_bot.py"])

if __name__ == "__main__":
    run()

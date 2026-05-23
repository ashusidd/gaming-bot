import requests
import os

def check_access():
    # Jo token abhi aapke paas hai (User Token), wahi rehne dein GitHub mein
    token = os.environ.get('FB_TOKEN')
    
    # Ye command aapke saare Pages ki list aur unke "Page Tokens" nikaal degi
    url = f"https://facebook.com{token}"
    
    r = requests.get(url)
    data = r.json()
    
    print("--- AAPKE PAGES KI LIST ---")
    print(data)
    print("---------------------------")

if __name__ == "__main__":
    check_access()

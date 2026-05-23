import requests
import os

def test_system():
    # GitHub Secrets se token uthana
    t = os.environ.get('FB_TOKEN')
    
    # URL (Isme koi galti nahi ho sakti ab)
    u = "https://facebook.com"
    p = {'access_token': t, 'fields': 'name,id'}
    
    try:
        r = requests.get(u, params=p)
        # Agar Facebook ne kuch bheja hai toh print hoga, warna error message aayega
        if r.status_code == 200:
            print("✅ SUCCESS! Facebook connect ho gaya.")
            print("Aapka Naam:", r.json().get('name'))
        else:
            print(f"❌ FACEBOOK ERROR: Status Code {r.status_code}")
            print("Detail:", r.text)
            
    except Exception as e:
        print(f"⚠️ SCRIPT ERROR: {e}")

if __name__ == "__main__":
    test_system()

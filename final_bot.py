import requests
import os

def check_access():
    # Token uthana
    t = os.environ.get('FB_TOKEN')
    
    # Simple URL - isme galti ka koi chance nahi
    u = "https://facebook.com"
    
    # Token ko params mein daal rahe hain taaki URL saaf rahe
    p = {'access_token': t}
    
    try:
        r = requests.get(u, params=p)
        d = r.json()
        
        print("--- RESULT ---")
        if 'data' in d:
            for page in d['data']:
                print(f"NAME: {page['name']}")
                print(f"TOKEN: {page['access_token']}")
                print("-" * 20)
        else:
            print("Nahi mila! Response ye aaya hai:", d)
            
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    check_access()

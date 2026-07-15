import os
import requests
import json
import sys

def get_nse_data():
    api_url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
    
    # Extract the cookie string dropped into GitHub Secrets securely
    manual_cookie = os.getenv("NSE_RAW_COOKIE")
    
    if not manual_cookie:
        print("CRITICAL ERROR: The NSE_COOKIE environment value is missing inside GitHub Settings!")
        sys.exit(1)
        
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.nseindia.com/option-chain",
        "X-Requested-With": "XMLHttpRequest",
        "Cookie": manual_cookie.strip() # Directly inject your human cookie token
    }
    
    try:
        print("Launching direct authenticated request block...")
        response = requests.get(api_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            payload = response.json()
            with open("data.json", "w") as f:
                json.dump(payload, f, indent=2)
            print("Successfully written authenticated dataset out to data.json.")
        else:
            print(f"Server rejected valid credential vector. HTTP Status: {response.status_code}")
            print(response.text[:200])
            sys.exit(1)
            
    except Exception as e:
        print(f"Network processing failed completely: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    get_nse_data()

import requests
import json
import sys
import time

def get_nse_data():
    # The base UI page we must load FIRST to receive authentic, signed session cookies
    home_url = "https://www.nseindia.com/option-chain"
    # The programmatic data route
    api_url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }
    
    session = requests.Session()
    session.headers.update(headers)
    
    try:
        # Step 1: Request the standard UI layer. This mimics human interaction and collects valid cookies.
        print("Visiting option-chain home to fetch cookies...")
        home_response = session.get(home_url, timeout=15)
        
        if home_response.status_code != 200:
            print(f"Could not initialize base session. Status: {home_response.status_code}")
            sys.exit(1)
            
        # Give the session cookies a tiny moment to register natively 
        time.sleep(2)
        
        # Step 2: Elevate headers explicitly for the structural JSON payload
        api_headers = {
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://www.nseindia.com/option-chain",
            "X-Requested-With": "XMLHttpRequest"
        }
        session.headers.update(api_headers)
        
        print("Requesting API data stream payload...")
        response = session.get(api_url, timeout=15)
        
        if response.status_code == 200:
            payload = response.json()
            
            # Save out to data.json so the index.html can pick it up locally
            with open("data.json", "w") as f:
                json.dump(payload, f, indent=2)
            print("Successfully updated data.json mapping.")
            
        else:
            print(f"NSE responded with error status: {response.status_code}")
            # If we hit an error page, print the first 200 chars to help debug
            print(response.text[:200])
            sys.exit(1)
            
    except Exception as e:
        print(f"Execution handling failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    get_nse_data()

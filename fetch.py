import requests
import json
import sys

def get_nse_data():
    home_url = "https://www.nseindia.com/option-chain"
    api_url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
    
    # Precise browser headers required to pass the cloud security inspection
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.nseindia.com/option-chain",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    session = requests.Session()
    session.headers.update(headers)
    
    try:
        # Step 1: Hit the specific option chain UI view to secure cookies
        session.get(home_url, timeout=15)
        
        # Step 2: Extract data with validation cookies attached
        response = session.get(api_url, timeout=15)
        
        if response.status_code == 200:
            payload = response.json()
            with open("data.json", "w") as f:
                json.dump(payload, f, indent=2)
            print("Successfully synchronized data.json.")
        else:
            print(f"NSE responded with error status: {response.status_code}")
            # Print response body snippets to assist troubleshooting if throttled
            print(response.text[:200])
            sys.exit(1)
            
    except Exception as e:
        print(f"Network processing failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    get_nse_data()

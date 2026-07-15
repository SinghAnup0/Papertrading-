import requests
import json
import sys

def get_nse_data():
    # Target endpoints
    home_url = "https://www.nseindia.com/"
    api_url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
    
    # Matching typical browser header finger-prints
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }
    
    session = requests.Session()
    session.headers.update(headers)
    
    try:
        # Step 1: Grab verification cookies from the home domain
        session.get(home_url, timeout=15)
        
        # Step 2: Request the actual JSON matrix payload
        response = session.get(api_url, timeout=15)
        
        if response.status_code == 200:
            # Confirming valid structural data was returned
            payload = response.json()
            with open("data.json", "w") as f:
                json.dump(payload, f, indent=2)
            print("Data stream synchronized successfully.")
        else:
            print(f"NSE responded with error status: {response.status_code}")
            sys.exit(1)
            
    except Exception as e:
        print(f"Network processing failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    get_nse_data()

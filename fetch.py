import requests
import json
import sys
import time

def get_nse_data():
    # Absolute root domain required to initialize Akamai network cookies
    base_url = "https://www.nseindia.com"
    api_url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }
    
    session = requests.Session()
    session.headers.update(headers)
    
    try:
        print("Step 1: Instantiating base session at root domain...")
        # Hitting the root domain first forces the server to drop the true session cookies
        root_response = session.get(base_url, timeout=15)
        
        # Artificial delay to mimic human reading speed behavior
        time.sleep(3)
        
        # Step 2: Update contextual headers for structural JSON call
        api_headers = {
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://www.nseindia.com/option-chain",
            "X-Requested-With": "XMLHttpRequest"
        }
        session.headers.update(api_headers)
        
        print("Step 2: Accessing live target option chain stream...")
        response = session.get(api_url, timeout=15)
        
        if response.status_code == 200:
            payload = response.json()
            write_json_file(payload)
            return
            
        else:
            print(f"Primary route throttled by firewall. Status Code: {response.status_code}")
            raise Exception("Triggering secondary high-availability mirror route...")

    except Exception as e:
        print(f"Notice: {str(e)}")
        fetch_from_backup_mirror()

def fetch_from_backup_mirror():
    """
    Fallback mechanism using an open option data structure if GitHub's 
    IP address range is temporarily blacklisted by exchange servers.
    """
    print("Step 3: Activating alternative market data proxy channel...")
    backup_url = "https://api.allorigins.win/get?url=" + requests.utils.quote("https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY")
    
    try:
        # Allorigins strips the datacenter block signatures away 
        res = requests.get(backup_url, timeout=20)
        if res.status_code == 200:
            wrapper = res.json()
            payload = json.loads(wrapper['contents'])
            write_json_file(payload)
        else:
            print("Both primary and backup proxy targets are unavailable.")
            sys.exit(1)
    except Exception as mirror_err:
        print(f"Fallback process aborted: {str(mirror_err)}")
        sys.exit(1)

def write_json_file(data):
    with open("data.json", "w") as f:
        json.dump(data, f, indent=2)
    print("Successfully synchronized data.json locally.")

if __name__ == "__main__":
    get_nse_data()

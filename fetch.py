import json
import sys
import time
import tls_client

def get_nse_data():
    base_url = "https://www.nseindia.com"
    api_url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
    
    # Initialize a browser engine mimicking an authentic desktop Chrome client layout
    session = tls_client.Session(
        client_identifier="chrome_120",
        random_tls_extensions_order=True
    )
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }
    
    try:
        print("Passing firewall using spoofed browser engine signatures...")
        # Step 1: Hit base to let the engine capture real session cookies
        session.get(base_url, headers=headers, timeout_seconds=15)
        
        # Micro delay mimicking human interaction
        time.sleep(2)
        
        # Step 2: Update headers for structural API acquisition path
        api_headers = {
            **headers,
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://www.nseindia.com/option-chain",
            "X-Requested-With": "XMLHttpRequest"
        }
        
        print("Extracting live NIFTY options chain data...")
        response = session.get(api_url, headers=api_headers, timeout_seconds=15)
        
        if response.status_code == 200:
            payload = response.json()
            with open("data.json", "w") as f:
                json.dump(payload, f, indent=2)
            print("Successfully refreshed data.json matrix metadata target.")
        else:
            print(f"Server responded with error status code: {response.status_code}")
            print(response.text[:200])
            sys.exit(1)
            
    except Exception as e:
        print(f"Scrape attempt terminated due to tracking fault: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    get_nse_data()

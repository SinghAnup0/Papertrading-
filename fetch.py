import json
import sys
from jugaad_data.nse import NSELive

def get_nse_data():
    try:
        print("Initializing jugaad-data engine...")
        n = NSELive()
        
        # Configure public request routing to bypass GitHub IP blockades
        proxy_url = "https://api.allorigins.win/get?url="
        target_api = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
        
        print("Extracting payload via high-availability bridge...")
        # Utilize internal session mapping to retrieve raw options matrix
        response = n.s.get(f"{proxy_url}{target_api}", timeout=25)
        
        if response.status_code == 200:
            wrapper = response.json()
            # Parse the nested content string returned by the bridge
            payload = json.loads(wrapper['contents'])
            
            if "records" in payload:
                with open("data.json", "w") as f:
                    json.dump(payload, f, indent=2)
                print("Successfully updated data.json payload storage.")
            else:
                print("Bridge returned data, but structural option records are missing.")
                sys.exit(1)
        else:
            print(f"Network bridge returned error code: {response.status_code}")
            sys.exit(1)
            
    except Exception as e:
        print(f"Extraction execution terminated: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    get_nse_data()

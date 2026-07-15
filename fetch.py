import json
import sys
from jugaad_data.nse import NSELive

def get_nse_data():
    try:
        print("Initializing jugaad-data live NSE connector...")
        n = NSELive()
        
        print("Downloading live NIFTY options chain payload...")
        # Fetching the live option chain matrix natively
        raw_data = n.option_chain("NIFTY")
        
        # Verify we received a valid data dictionary
        if "records" in raw_data and "filtered" in raw_data:
            with open("data.json", "w") as f:
                json.dump(raw_data, f, indent=2)
            print("Successfully refreshed data.json matrix mapping via backend.")
        else:
            print("Error: Received structural response, but option chain blocks were missing.")
            sys.exit(1)
            
    except Exception as e:
        print(f"Jugaad-data connection pipeline failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    get_nse_data()

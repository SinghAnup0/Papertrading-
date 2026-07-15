# fetch_data.py
from datetime import date
from jugaad_data.nse import stock_df
import os

# Create a folder to store our data
os.makedirs("data", exist_ok=True)

# Fetch historical data for SBIN
try:
    print("Fetching data...")
    df = stock_df(
        symbol="SBIN", 
        from_date=date(2026, 1, 1), 
        to_date=date(2026, 1, 30), 
        series="EQ"
    )
    # Save to CSV
    output_path = "data/SBIN_data.csv"
    df.to_csv(output_path, index=False)
    print(f"Successfully saved data to {output_path}!")
except Exception as e:
    print(f"Error fetching data: {e}")

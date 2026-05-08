# TTC Subway Delay Data Cleaning Script

# Author: Sarah Masrie
# Date: May 2026
# Description:
# Cleans and transforms TTC subway delay data for Power BI analysis.
# Creates datetime features and delay severity categories.

import pandas as pd

NO_DELAY_LIMIT = 0
SMALL_DELAY_LIMIT = 5
MEDIUM_DELAY_LIMIT = 15

# Load Data
ttc_data = pd.read_csv("./data/ttc_subway_delay.csv")

# Basic Cleaning

# Fill missing values
ttc_data["Bound"] = ttc_data["Bound"].fillna("Unknown")
ttc_data["Line"] = ttc_data["Line"].fillna("Unknown")

# Numeric field validation
ttc_data["Min Delay"] = pd.to_numeric(ttc_data["Min Delay"], errors="coerce").fillna(0)
ttc_data["Min Gap"] = pd.to_numeric(ttc_data["Min Gap"], errors="coerce").fillna(0)
ttc_data["Vehicle"] = pd.to_numeric(ttc_data["Vehicle"], errors="coerce").fillna(0)

# Combine Date + Time into one datetime column
ttc_data["DateTime"] = pd.to_datetime(ttc_data["Date"] + " " + ttc_data["Time"])

# Drop the original/irrelevant columns
ttc_data = ttc_data.drop(columns=["_id", "Date", "Time"])

# Split the date for Power BI
ttc_data["Year"] = ttc_data["DateTime"].dt.year
ttc_data["Month"] = ttc_data["DateTime"].dt.month
ttc_data["Hour"] = ttc_data["DateTime"].dt.hour
ttc_data["Weekday"] = ttc_data["DateTime"].dt.day_name()

# Delay Categorization
def categorize_delay(delay_minutes):
    if delay_minutes == NO_DELAY_LIMIT:
        return "No Delay"
    elif delay_minutes <= SMALL_DELAY_LIMIT:
        return "Small"
    elif delay_minutes <= MEDIUM_DELAY_LIMIT:
        return "Medium"
    else:
        return "Severe"

ttc_data["Delay Category"] = ttc_data["Min Delay"].apply(categorize_delay)

# Output clean file
output_file = "./data/ttc_cleaned.csv"
ttc_data.to_csv(output_file, index=False)


# Debug Output
print("FIRST 5 ROWS:")
print(ttc_data.head())

print("\nDATASET INFO:")
print(ttc_data.info())

print("\nDataset cleaned successfully.")
print(f"Cleaned file saved as: {output_file}")
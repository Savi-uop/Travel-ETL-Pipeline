import pandas as pd

def clean_data(file_path):
    df = pd.read_csv(file_path)
    initial_count = len(df)

    # 1. Remove Exact Duplicates
    df = df.drop_duplicates(subset=['booking_id'])

    # 2. Standardize Formats
    df['destination'] = df['destination'].str.title().str.strip()
    df['booking_date'] = pd.to_datetime(df['booking_date'], errors='coerce')
    
    # 3. Handle Missing Values & Outliers (The Validation Logic)
    # Define "Rejected" as records with null dates or negative prices
    rejected_mask = (df['booking_date'].isna()) | (df['price'] <= 0) | (df['price'].isna())
    
    rejected_df = df[rejected_mask]
    clean_df = df[~rejected_mask].copy()

    # Log Rejected Records
    if not rejected_df.empty:
        rejected_df.to_csv('rejected_records.log', index=False)
        print(f" Logged {len(rejected_df)} rejected records to rejected_records.log")

    print(f" Cleaned {len(clean_df)} records. (Removed {initial_count - len(clean_df)} total)")
    return clean_df
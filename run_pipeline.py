from src.extract import upload_to_s3, download_from_s3
from src.transform import clean_data
from src.load import load_to_postgres
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    RAW_FILE = 'raw_travel_bookings.csv'
    BUCKET = os.getenv('S3_BUCKET_NAME')

    print("--- Starting ETL Pipeline ---")
    
    # 1. Extract: Upload to S3, then pull it back as if from a cloud source
    upload_to_s3(RAW_FILE, BUCKET)
    cloud_file = download_from_s3(RAW_FILE, BUCKET)

    # 2. Transform: Clean and validate
    clean_df = clean_data(cloud_file)

    # 3. Load: Push to PostgreSQL
    load_to_postgres(clean_df, 'bookings')

    print("--- Pipeline Completed Successfully ---")

if __name__ == "__main__":
    main()
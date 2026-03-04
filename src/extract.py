import os
import shutil
from dotenv import load_dotenv

load_dotenv()

class MockS3Client:
    """
    This class mimics the boto3 S3 client behavior for local testing 
    without requiring AWS credentials or Docker.
    """
    def __init__(self):
        self.base_dir = "mock_s3_bucket"
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)
            print(f" Created local mock S3 bucket: {self.base_dir}")

    def upload_file(self, local_path, bucket_name, object_name):
        # In a real S3, this uploads to the cloud. 
        # Here, we copy it to our 'mock_s3_bucket' folder.
        destination = os.path.join(self.base_dir, object_name)
        shutil.copy(local_path, destination)
        print(f" [MOCK S3] Uploaded {local_path} to {bucket_name}/{object_name}")

    def download_file(self, bucket_name, object_name, local_destination):
        # In a real S3, this pulls from the cloud.
        source = os.path.join(self.base_dir, object_name)
        if os.path.exists(source):
            shutil.copy(source, local_destination)
            print(f" [MOCK S3] Downloaded {object_name} from {bucket_name}")
        else:
            print(f" Error: {object_name} not found in mock bucket.")

def get_s3_client():
    # If we had AWS, we would return boto3.client('s3').
    # Since we are mocking it, we return our custom MockS3Client.
    return MockS3Client()

def upload_to_s3(file_name, bucket):
    s3 = get_s3_client()
    s3.upload_file(file_name, bucket, file_name)

def download_from_s3(file_name, bucket):
    target_path = f"downloaded_{file_name}"
    s3 = get_s3_client()
    s3.download_file(bucket, file_name, target_path)
    return target_path
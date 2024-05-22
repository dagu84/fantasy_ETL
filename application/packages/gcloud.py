import os
from google.cloud import storage

# Google Credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/dg/Desktop/DG/data_science/gcp/ff-nfl-e6db3eb1124e.json'

# Initialize the Google Cloud Storage client
storage_client = storage.Client()

def upload_file_to_bucket(file_path, blob_name, bucket_name):
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_string(file_path)
        return True

    except Exception as e:
        print(e)
        return False


def download_from_bucket(file_path, blob_name, bucket_name):
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        with open(file_path, 'wb') as f:
            storage_client.download_blob_to_file(blob, f)
        return True

    except Exception as e:
        print(e)
        return False

def upload_string_to_bucket(string, bucket_name, blob_name):
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(string, content_type='text/csv')

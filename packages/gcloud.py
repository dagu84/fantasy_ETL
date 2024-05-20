import os
import datetime
from google.cloud import storage

# Google Credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/dg/Desktop/DG/data_science/gcp/ff-nfl-e6db3eb1124e.json'

# Bucket temporary filepath
current_date = datetime.date.today()
file_path = file_path = os.path.join(os.path.dirname(__file__), 'raw_data', f'{current_date}_players.csv')

# Initialize the Google Cloud Storage client
storage_client = storage.Client()

def upload_to_bucket(file_path, blob_name, bucket_name):
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_path)
        return True

    except Exception as e:
        print(e)
        return False


def download_from_bucket(blob_name, bucket_name):
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        with open(file_path, 'wb') as f:
            storage_client.download_blob_to_file(blob, f)
        return True

    except Exception as e:
        print(e)
        return False

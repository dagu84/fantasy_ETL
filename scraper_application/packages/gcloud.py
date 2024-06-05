import os
import pandas as pd
from google.cloud import storage

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


def download_csv_to_dataframe(bucket_name, blob_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    csv_string = blob.download_as_text()
    df = pd.read_csv(pd.compat.StringIO(csv_string))
    return df

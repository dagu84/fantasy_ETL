import os
import datetime
import pandas as pd
from dotenv import load_dotenv
from google.cloud import storage
from packages.gcloud import upload_to_bucket
from packages.sleeper_api import status, player
from packages.sql import create_connection, commit_close, insert
from packages.transformation import player_transform


load_dotenv()
current_date = datetime.date.today()
username = os.getenv('USERNAME')
league = os.getenv('LEAGUE')
bucket = os.getenv('BUCKET_NAME')


if __name__=="__main__":
    if status(username) == 200:

        #Check API status
        print('API call successfull.')
        data = player()

        #Transform Data and save Temporarily
        df = player_transform(data)
        df.to_csv(f'../raw_data/csv/{current_date}_player.csv')
        print('File temporarily saved.')

        #Insert data into db
        connection = create_connection()
        insert(connection, df, 'players')
        commit_close(connection)

        #Connect and update player historicals bucket
        upload_to_bucket(f'../raw_data/csv/{current_date}_player.csv', blob_name=(f'{current_date}_player.csv'), bucket_name=bucket)

        #Commit and close
        print('File executed successfully.')

    else:
        print(status(username))
        print("Failed API call.")

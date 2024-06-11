import os
import io
from flask import Flask
import datetime
from packages.gcloud import upload_string_to_bucket
from packages.sleeper_api import status, player, user, roster
from packages.transformation import player_transform, users_transform, roster_transform


current_date = datetime.date.today()
username = os.getenv('USERNAME')
league = os.getenv('LEAGUE')
bucket_hist = os.getenv('BUCKET_NAME_HIST')
bucket_current = os.getenv('BUCKET_NAME_CURRENT')


app = Flask(__name__)


@app.route('/')
def index():
    if status(username) == 200:

        #Check API status
        print('API call successfull.')
        players = player()
        users = user(league)
        rosters = roster(league)

        #Transform Data and save temporarily as a string
        df = player_transform(players)
        #Adding date column for tracking
        df['date'] = current_date
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        player_data = csv_buffer.getvalue()

        df = users_transform(users, rosters)
        df['date'] = current_date
        #Adding date column for tracking
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        user_data = csv_buffer.getvalue()

        df = roster_transform(rosters)
        df['date'] = current_date
        #Adding date column for tracking
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        rosters_data = csv_buffer.getvalue()

        print('Data prepared.')

        #Connect and update player historicals bucket
        upload_string_to_bucket(player_data, blob_name=(f'{current_date}_player.csv'), bucket_name=bucket_hist)
        upload_string_to_bucket(user_data, blob_name=(f'{current_date}_users.csv'), bucket_name=bucket_hist)
        upload_string_to_bucket(rosters_data, blob_name=(f'{current_date}_rosters.csv'), bucket_name=bucket_hist)

        print('Historical files uploaded.')

        #Connect and update player current bucket
        upload_string_to_bucket(player_data, blob_name=('player.csv'), bucket_name=bucket_current)
        upload_string_to_bucket(user_data, blob_name=('users.csv'), bucket_name=bucket_current)
        upload_string_to_bucket(rosters_data, blob_name=('rosters.csv'), bucket_name=bucket_current)

        print('File executed successfully.')

    else:
        print(status(username))
        print("Failed API call.")

    return 'File executed.'


if __name__=="__main__":
    # print("docker file executed.")
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

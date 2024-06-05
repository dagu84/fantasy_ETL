import os
import io
from flask import Flask
import datetime
from dotenv import load_dotenv
from packages.gcloud import upload_string_to_bucket
from packages.sleeper_api import status, player, user, roster
from packages.transformation import player_transform, users_transform, roster_transform


current_date = datetime.date.today()
username = os.getenv('USERNAME')
league = os.getenv('LEAGUE')
bucket = os.getenv('BUCKET_NAME')


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
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        player_data = csv_buffer.getvalue()

        df = users_transform(users, rosters)
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        user_data = csv_buffer.getvalue()

        df = roster_transform(rosters)
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        rosters_data = csv_buffer.getvalue()

        print('Data prepared.')


        #Connect and update player historicals bucket (PLAYERS)
        upload_string_to_bucket(player_data, blob_name=(f'{current_date}_player.csv'), bucket_name=bucket)
        upload_string_to_bucket(user_data, blob_name=(f'{current_date}_users.csv'), bucket_name=bucket)
        upload_string_to_bucket(rosters_data, blob_name=(f'{current_date}_rosters.csv'), bucket_name=bucket)

        print('File executed successfully.')

    else:
        print(status(username))
        print("Failed API call.")

    return 'File executed.'


if __name__=="__main__":
    # print("docker file executed.")
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

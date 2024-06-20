import os
import io
import datetime
import pandas as pd
from flask import Flask
from dotenv import load_dotenv
from packages.sleeper_api import status, player, user, roster
from packages.transformation import player_transform, users_transform, roster_transform
from packages.scraper import performance_scrape, status_web, status_web, combine_scrape, draft_scrape
from packages.gcloud import upload_string_to_bucket, download_csv_to_dataframe
from packages.transformation import qb_transform, pass_catcher_transform, rb_transform, draft_transform, combine_transform


load_dotenv()
current_date = datetime.date.today()
year = 2019
username = os.getenv('USERNAME')
league = os.getenv('LEAGUE')
bucket = os.getenv('BUCKET_NAME_SCRAPE')
bucket_hist = os.getenv('BUCKET_NAME_HIST')
bucket_current = os.getenv('BUCKET_NAME_CURRENT')
bucket_name = os.getenv('BUCKET_NAME_SCRAPE_HIST')

schedule = f'schedule_dates_{year}.csv'
app = Flask(__name__)


def week_counter(df):
    df['date'] = pd.to_datetime(df['date'])
    week = df.loc[df['date'] == current_date, 'week']
    if not week.empty:
        return week.iloc[0]
    else:
        return "Week not found for the current date."


@app.route('/')
def index():
    return 'root endpoint.'


@app.route('/api')
def api():
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


@app.route('/scrape_cd')
def scrape_cd():
    url = 'https://www.wikipedia.org/'
    if status_web(url) == 200:

        # Check Website status
        print('Website connection successfull.')

        # Scraping table data
        draft = draft_scrape(year)
        combine = combine_scrape(year)

        # Transform Data and save temporarily as a string
        df = draft_transform(draft)
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        draft = csv_buffer.getvalue()

        df = combine_transform(combine)
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        combine = csv_buffer.getvalue()

        print('Data prepared.')

        # Connect and update player performance bucket
        upload_string_to_bucket(draft, blob_name=(f'draft_{year}.csv'), bucket_name=bucket_name)
        upload_string_to_bucket(combine, blob_name=(f'combine_{year}.csv'), bucket_name=bucket_name)

        print('File executed successfully.')

    else:
        print('Connection failed')

    return 'File executed.'


@app.route('/scrape_ff')
def scrape_ff():
    df = download_csv_to_dataframe(bucket, schedule)
    week = df.loc[df['date'] == current_date, 'week']
    if not week.empty:

        # Check Website status
        print('Website connection successfull.')

        # Extracting the correct schedule week
        week = week_counter(df)

        # Scraping table data
        qb_url = f'https://www.fantasypros.com/nfl/stats/qb.php?year={year}&week={week}&scoring=PPR&range=week'
        rb_url = f'https://www.fantasypros.com/nfl/stats/rb.php?year={year}&week={week}&scoring=PPR&range=week'
        wr_url = f'https://www.fantasypros.com/nfl/stats/wr.php?year={year}&week={week}&scoring=PPR&range=week'
        te_url = f'https://www.fantasypros.com/nfl/stats/te.php?year={year}&week={week}&scoring=PPR&range=week'

        qb = performance_scrape(qb_url)
        rb = performance_scrape(rb_url)
        wr = performance_scrape(wr_url)
        te = performance_scrape(te_url)

        print('Data scraped successfully.')

        # Transform Data and save temporarily as a string
        df = qb_transform(qb, week)
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        qb = csv_buffer.getvalue()

        rb = rb_transform(rb, week)
        pass_catch = pass_catcher_transform(wr, te, week)
        df = pd.concat([rb, pass_catch], ignore_index=True)
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        skill_position = csv_buffer.getvalue()

        print('Data prepared.')

        # Connect and update player performance bucket
        upload_string_to_bucket(qb, blob_name=(f'week{current_date}_qb.csv'), bucket_name=bucket)
        upload_string_to_bucket(skill_position, blob_name=(f'week{current_date}_skill.csv'), bucket_name=bucket)

        print('File executed successfully.')

    else:
        print('Date not included.')

    return 'File executed.'


@app.route('/scrape_league')
def scrape_league():
    pass


if __name__=="__main__":
    # print("docker file executed.")
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

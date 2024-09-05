import os
import io
import datetime
from flask import Flask
import pandas as pd
from monolith.packages.scraper import performance_scrape, status_web, pre_rankings
from packages.gcloud import upload_string_to_bucket, download_csv_to_dataframe
from packages.transformation import qb_transform, pass_catcher_transform, rb_transform


current_date = datetime.date.today()
year = current_date.year

bucket = os.getenv('BUCKET_NAME_SCRAPE')

homepage = f'https://www.fantasypros.com/nfl/stats/wr.php?year=2023&scoring=PPR&range=full'
schedule = f'schedule_dates_{year}.csv'


def week_counter(df):
    try:
        df['date'] = pd.to_datetime(df['date'])
        week = df.loc[df['date'] == current_date, 'week']
        if not week.empty:
            return week.iloc[0]
        else:
            return "Week not found for the current date."

    except Exception:
        return 1


app = Flask(__name__)


@app.route('/')
def index():
    if status_web(homepage) == 200:

        # Check Website status
        print('Website connection successfull.')

        # Import the schedule dataframe
        df = download_csv_to_dataframe(bucket, schedule)

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
        print('Connection failed')

    return 'Script executed.'


# @app.route('/rankings')
# def ranking():
#     if status_web('https://www.cbssports.com/fantasy/football/rankings/ppr/flex/weekly/') == 200:

#         # Check Website status
#         print('Website connection successfull.')

#         df = pre_rankings('https://www.cbssports.com/fantasy/football/rankings/ppr/flex/weekly/')

#         csv_buffer = io.StringIO()
#         df.to_csv(csv_buffer, index=False)
#         df = csv_buffer.getvalue()

#         print('Data prepared.')

#         # Connect and update player performance bucket
#         upload_string_to_bucket(df, blob_name=(f'week{current_date}_rankings.csv'), bucket_name=bucket)

#         print('File executed successfully.')

#     else:
#         print('Connection failed')

#     return 'Script executed.'


@app.route('/test')
def whatever():
    df = pd.DataFrame()
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    df = csv_buffer.getvalue()
    upload_string_to_bucket(df, blob_name='testing', bucket_name=bucket)

    return 'Script executed.'


if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

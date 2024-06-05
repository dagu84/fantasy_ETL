import os
import io
import datetime
import pandas as pd
from dotenv import load_dotenv
from scraper_application.packages.scraper import performance_scrape, status_web
from scraper_application.packages.gcloud import upload_string_to_bucket, download_csv_to_dataframe


load_dotenv()
current_date = datetime.date.today()
year = current_date.year
username = os.getenv('USERNAME')
league = os.getenv('LEAGUE')
bucket_save = os.getenv('BUCKET_NAME2')
bucket_load = os.getenv('BUCKET_NAME')
homepage = f'https://www.fantasypros.com/nfl/stats/wr.php?year={year}&scoring=PPR&range=full'
schedule = f'schedule_dates_{year}.csv'

def week_counter(df):
    df['date'] = pd.to_datetime(df['date'])
    week = df.loc[df['date'] == current_date, 'week']
    return week


if __name__=="__main__":
    if status_web(homepage) == 200:

        # Check Website status
        print('Website connection successfull.')

        # Import the schedule dataframe
        df = download_csv_to_dataframe(bucket_load, schedule)

        # Extracting the correct schedule week
        week = week_counter(df)

        # Scraping table data
        qb_url = f'https://www.fantasypros.com/nfl/stats/qb.php?year={year}&week={week}&scoring=PPR&range=week'
        rb_url = f'https://www.fantasypros.com/nfl/stats/qb.php?year={year}&week={week}&scoring=PPR&range=week'
        wr_url = f'https://www.fantasypros.com/nfl/stats/qb.php?year={year}&week={week}&scoring=PPR&range=week'
        te_url = f'https://www.fantasypros.com/nfl/stats/qb.php?year={year}&week={week}&scoring=PPR&range=week'

        qb = performance_scrape(qb_url)
        rb = performance_scrape(rb_url)
        wr = performance_scrape(wr_url)
        te = performance_scrape(te_url)

        print('Data scraped successfully.')

        # Transform Data and save temporarily as a string
        # This will be for transformation
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        qb = csv_buffer.getvalue()

        # This will be for transformation
        df = pd.concat([rb, wr, te], ignore_index=True)
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        skill_position = csv_buffer.getvalue()

        print('Data prepared.')

        # Connect and update player performance bucket
        upload_string_to_bucket(qb, blob_name=(f'week{current_date}_qb.csv'), bucket_name=bucket_save)
        upload_string_to_bucket(skill_position, blob_name=(f'week{current_date}_skill.csv'), bucket_name=bucket_save)

        print('File executed successfully.')

    else:
        print('Connection failed')

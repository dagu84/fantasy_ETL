import os
import io
import datetime
from flask import Flask
from dotenv import load_dotenv
from packages.scraper import status_web, combine_scrape, draft_scrape
from packages.transformation import draft_transform, combine_transform
from packages.gcloud import upload_string_to_bucket

current_date = datetime.date.today()
year = current_date.year

load_dotenv()
bucket_name = os.getenv('BUCKET_NAME_SCRAPE_HIST')
url = 'https://www.wikipedia.org/'


app = Flask(__name__)


@app.route('/')
def index():
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


if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

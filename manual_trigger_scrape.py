import os
import io
import datetime
from dotenv import load_dotenv
from scraper_application.packages.scraper import performance_scrape
from scraper_application.packages.gcloud import upload_string_to_bucket


load_dotenv()
current_date = datetime.date.today()
username = os.getenv('USERNAME')
league = os.getenv('LEAGUE')
bucket = os.getenv('BUCKET_NAME')


if __name__=="__main__":

    # Pulling in scraped data
    qb = performance_scrape()
    rb = performance_scrape()
    wr = performance_scrape()
    te = performance_scrape()

    # Tranforming and preparing the data for injestion

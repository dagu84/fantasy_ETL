import os
import datetime
from packages.scraper import performance_scrape
from packages.gcloud import upload_string_to_bucket

current_date = datetime.date.today()
bucket = os.getenv('BUCKET_NAME')

def url_creator():
    pass

if __name__=="__main__":

    # Pulling in scraped data
    qb = performance_scrape()
    rb = performance_scrape()
    wr = performance_scrape()
    te = performance_scrape()

    # Tranforming and preparing the data for injestion

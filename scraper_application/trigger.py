from packages.scraper import performance_scrape
from packages.gcloud import upload_string_to_bucket

if __name__=="__main__":

    # Pulling in scraped data
    qb = performance_scrape()
    rb = performance_scrape()
    wr = performance_scrape()
    te = performance_scrape()

    # Tranforming and preparing the data for injestion

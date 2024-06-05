import requests
import pandas as pd
from bs4 import BeautifulSoup

def status_web(url):
    response = requests.get(url)
    return response

def performance_scrape(url):

    # Calling website
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Processing scraped data into rows
    table = soup.find('table', {'id': 'data'})
    headers = []
    for th in table.find_all('th'):
        headers.append(th.text.strip())

    rows = []
    for tr in table.find_all('tr'):
        cells = tr.find_all(['td', 'th'])
        row = [cell.text.strip() for cell in cells]
        if row:
            rows.append(row)

    # Formatting rows into dataframe
    df = pd.DataFrame(rows, columns=headers)

    return df

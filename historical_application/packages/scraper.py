import requests
import pandas as pd
from bs4 import BeautifulSoup

def status_web(url):
    request = requests.get(url)
    return request.status_code


def combine_scrape(year):
    url = f'https://www.pro-football-reference.com/draft/{year}-combine.htm'

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table', {'id': 'combine'})
    headers = []
    for th in table.find('thead').find_all('th'):
        headers.append(th.text.strip())

    rows = []
    for tr in table.find('tbody').find_all('tr'):
        cells = tr.find_all(['td', 'th'])
        row = []
        for cell in cells:
            if cell.find('a'):
                row.append(cell.find('a').text.strip())
            else:
                row.append(cell.text.strip())
        while len(row) < len(headers):
            row.append('')
        rows.append(row)

    df = pd.DataFrame(rows, columns=headers)

    return df


def draft_scrape(year):
    url = f'https://en.wikipedia.org/wiki/{year}_NFL_draft'

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table', attrs={'class': 'wikitable sortable plainrowheaders'})

    headers = []
    rows = []

    for th in table.find_all('th'):
        header = th.get_text(strip=True)
        headers.append(header)

    headers = headers[0:9]

    for tr in table.find_all('tr')[1:]:
        cells = tr.find_all(['th', 'td'])
        row = [cell.get_text(strip=True) for cell in cells]
        rows.append(row)

    df = pd.DataFrame(rows, columns=headers)

    return df

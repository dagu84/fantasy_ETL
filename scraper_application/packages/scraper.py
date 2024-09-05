import re
import requests
import pandas as pd
from bs4 import BeautifulSoup

url = f'https://www.fantasypros.com/nfl/stats/wr.php?year=2023&scoring=PPR&range=full'

def status_web(url):
    request = requests.get(url)
    return request.status_code

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

def pre_rankings(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    experts_column = soup.find('div', attrs={'class': 'experts-column triple'})
    player_rows = experts_column.find_all('div', attrs={'class': 'player-row'})
    player_data = []

    for row in player_rows:
        rank = row.find('div', attrs={'class': 'rank'}).text.strip() if row.find('div', attrs={'class': 'rank'}) else None

        player = row.find('div', attrs={'class': 'player'}).text.strip() if row.find('div', attrs={'class': 'player'}) else None
        if player:
            player = re.sub(r'\s+(WR|TE|RB)\s*', '', player).strip()
            player = player.replace('\n', '').strip()

        team_position = row.find('span', attrs={'class': 'team position'}).text.strip() if row.find('span', attrs={'class': 'team position'}) else None
        player_stats = row.find('div', attrs={'class': 'player-stats'}).text.strip() if row.find('div', attrs={'class': 'player-stats'}) else None
        if player_stats:
            player_stats = player_stats.replace('@', '').strip()

        player_data.append([rank, player, team_position, player_stats])

    df = pd.DataFrame(player_data, columns=['Rank', 'Player', 'Team Position', 'Opponent'])

    return df

if __name__=="__main__":
    print(f"{status_web(url)}, the api call was successfull.")

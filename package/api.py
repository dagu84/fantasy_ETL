import requests

def status(username):
    request = requests.get(f'https://api.sleeper.app/v1/user/{username}')
    return request.status_code

def roster(league):
    request = requests.get(f'https://api.sleeper.app/v1/league/{league}/rosters')
    return request.json()

def player():
    request = requests.get('https://api.sleeper.app/v1/players/nfl')
    return request.json()

import os
from package.api import status, roster, player
from package.sql import create_connection, commit_close, temp_table
from package.transformation import player_table

username = os.environ.get('USERNAME')
league = os.environ.get('LEAGUE')

if __name__=="__main__":
    if status(username) == 200:
        print('API call successfull.')
        data = player()
        df = player_table(data)
        connection = create_connection()
        temp_table(connection, df)
        commit_close(connection)
        print('File executed successfully.')


    else:
        print(status(username))
        print("Failed API call.")

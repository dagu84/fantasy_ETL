import os
import sqlite3
import pandas as pd

def create_connection():
    # Creating a file path to the data storage directory
    file_path = file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'raw_data', 'sql_db')

    # Creating a connection to the sql file, if it doens't exist it will create the db file
    connection = sqlite3.connect(file_path)

    return connection


def commit_close(connection):
    # Committing the sql query/statement to the database
    connection.commit()

    # Closing the connection to the database
    connection.close()

    return 'Connection committed and closed'


def insert(connection, df, table):
    df.to_sql(name=table, con=connection, if_exists='replace', index=False)
    return print('Data inserted successfully.')

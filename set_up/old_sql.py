import sqlite3

def player_table(connection):
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players(
            id INTEGER PRIMARY KEY,
            first_name VARCHAR,
            last_name VARCHAR,
            position VARCHAR,
            age INTEGER,
            team VARCHAR,
            depth_chart_order INTEGER,
            search_rank INTEGER,
            college VARCHAR,
            years_exp INTEGER,
            status VARCHAR)''')
    return cursor

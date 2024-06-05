import numpy as np
import pandas as pd

def player_transform(data):

    df = pd.DataFrame(data)
    df = df.T

    df.reset_index(inplace=True)
    df.rename(columns={'index':'id'}, inplace=True)
    df = df[['id', 'first_name', 'last_name', 'position', 'age', 'team', 'depth_chart_order', 'search_rank', 'college', 'years_exp', 'status']]

    pd.set_option('future.no_silent_downcasting', True)
    df.replace('None', np.nan, inplace=True)

    return df


def users_transform(data1, data2):

    #Using data from the users api
    df = pd.DataFrame(data1)
    df = df[['user_id', 'metadata', 'display_name']]
    df['team_name'] = [met['team_name'] for met in df['metadata']]

    #Using the data from the roster api
    df2 = pd.DataFrame(data2)
    settings_df = pd.json_normalize(df2['settings'])
    df2 = pd.concat([df2.drop(columns='settings'), settings_df], axis=1)

    #Concating the two dataframes
    df = pd.concat([df, df2[['total_moves', 'wins', 'ties', 'losses', 'waiver_position', 'fpts']]])

    return df


def roster_transform(data):
    df = pd.DataFrame(data)

    expanded_rows = []
    for idx, row in df.iterrows():
        for player in row['players']:
            expanded_row = row.to_dict()
            expanded_row['player'] = player
            expanded_row['type'] = 'player'
            expanded_rows.append(expanded_row)
        for starter in row['starters']:
            expanded_row = row.to_dict()
            expanded_row['player'] = starter
            expanded_row['type'] = 'starter'
            expanded_rows.append(expanded_row)

    df = pd.DataFrame(expanded_rows)
    df = df[['player', 'owner_id', 'type']]
    df.rename(columns={'player':'player_id', 'owner_id':'user_id'}, inplace=True)

    return df

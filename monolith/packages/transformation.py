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


def draft_transform(data):
    data[['Rnd.', 'Pick No.']] = data[['Rnd.', 'Pick No.']].astype(str)
    to_drop = data[data[['Rnd.', 'Pick No.']].apply(lambda x: x.str.contains(r'[^0-9-]')).any(axis=1)].index
    data = data.drop(to_drop)

    data['Rnd.'] = data['Rnd.'].astype(int)
    data['Pick No.'] = data['Pick No.'].astype(int)

    return data


def combine_transform(data):
    data['Ht'] = data['Ht'].str.replace('-', '.', regex=False)
    data = data.rename(columns={'Drafted (tm/rnd/yr)':'Drafted'})

    to_drop = data[data['Ht']=='Ht'].index
    data = data.drop(to_drop)

    data = data.replace(['', ' ', None], np.nan)
    data[['Ht', '40yd', 'Vertical', '3Cone', 'Shuttle']] = data[['Ht', '40yd', 'Vertical', '3Cone', 'Shuttle']].astype(float)

    return data


def qb_transform(data, week):
    # Transforms the raw quarterback scraped table into formatted dataframe
    data = data.drop(columns=['Rank', 'G', 'FPTS/G', 'ROST'])
    data = data.drop(index=[0,1]).reset_index(drop=True)
    column = ['id', 'passing_cmp', 'passing_att', 'passing_percent', 'passing_yards', 'passing_y/a', 'passing_td', 'passing_int',
              'sacks', 'rushing_att', 'rushing_yards', 'rushing_td', 'fumbles_lost', 'fantasy_points']
    data.columns = column
    data[['passing_cmp', 'passing_att', 'passing_yards', 'passing_td', 'passing_int', 'sacks', 'rushing_att', 'rushing_yards', 'rushing_td', 'fumbles_lost']] = data[['passing_cmp', 'passing_att', 'passing_yards', 'passing_td', 'passing_int', 'sacks', 'rushing_att', 'rushing_yards', 'rushing_td', 'fumbles_lost']].astype(int)
    data[['passing_percent', 'passing_y/a', 'fantasy_points']] = data[['passing_percent', 'passing_y/a', 'fantasy_points']].astype(float)
    data['total_td'] = data['passing_td'] + data['rushing_td']
    data['total_yards'] = data['passing_yards'] + data['rushing_yards']
    data['week'] = week

    return data


def pass_catcher_transform(wr, te, week):
    # Transforms the raw pass catcher scraped table into formatted dataframe
    wr = wr.drop(columns=['Rank', 'G', 'FPTS/G', 'ROST', 'LG', '20+'])
    wr = wr.drop(index=[0,1]).reset_index(drop=True)

    te = te.drop(columns=['Rank', 'G', 'FPTS/G', 'ROST', 'LG', '20+'])
    te = te.drop(index=[0,1]).reset_index(drop=True)
    data = pd.concat([wr, te], ignore_index=True)

    column = ['id', 'receiving_rec', 'receiving_targets', 'receiving_yards', 'receiving_y/r', 'receiving_td',
              'rushing_att', 'rushing_yards', 'rushing_td', 'fumbles_lost', 'fantasy_points']
    data.columns = column

    data[['receiving_rec', 'receiving_targets', 'receiving_yards', 'receiving_td', 'rushing_att', 'rushing_yards', 'rushing_td', 'fumbles_lost']] = data[['receiving_rec', 'receiving_targets', 'receiving_yards', 'receiving_td', 'rushing_att', 'rushing_yards', 'rushing_td', 'fumbles_lost']].astype(int)
    data[['receiving_y/r', 'fantasy_points']] = data[['receiving_y/r', 'fantasy_points']].astype(float)

    data['total_td'] = data['receiving_td'] + data['rushing_td']
    data['total_yards'] = data['receiving_yards'] + data['rushing_yards']
    data['rushing_y/a'] = round(data['rushing_yards'] / data['rushing_att'], 1)
    data['week'] = week

    return data


def rb_transform(data, week):
    # Transforms the raw skill rb scraped table into formatted dataframe
    data = data.drop(columns=['Rank', 'G', 'FPTS/G', 'ROST', 'LG', '20+'])
    data = data.drop(index=[0,1]).reset_index(drop=True)

    column = ['id', 'rushing_att', 'rushing_yards', 'rushing_y/a', 'rushing_td',
              'receiving_rec', 'receiving_targets', 'receiving_yards', 'receiving_y/r', 'receiving_td', 'fumbles_lost', 'fantasy_points']
    data.columns = column

    data[['receiving_rec', 'receiving_targets', 'receiving_yards', 'receiving_td', 'rushing_att', 'rushing_yards', 'rushing_td', 'fumbles_lost']] = data[['receiving_rec', 'receiving_targets', 'receiving_yards', 'receiving_td', 'rushing_att', 'rushing_yards', 'rushing_td', 'fumbles_lost']].astype(int)
    data[['receiving_y/r', 'rushing_y/a', 'fantasy_points']] = data[['receiving_y/r', 'rushing_y/a', 'fantasy_points']].astype(float)

    data['total_td'] = data['receiving_td'] + data['rushing_td']
    data['total_yards'] = data['receiving_yards'] + data['rushing_yards']
    data['week'] = week

    return data

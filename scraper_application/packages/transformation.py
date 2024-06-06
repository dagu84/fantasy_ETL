import numpy as np
import pandas as pd

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

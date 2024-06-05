import numpy as np
import pandas as pd

def qb_transform(data, week):
    # Transforms the raw quarterback scraped table into formatted dataframe
    data.drop(columns=['Rank', 'G', 'FPTS/G', 'ROST'], inplace=True)
    data.drop(index=[0,1]).reset_index(drop=True, inplace=True)
    column = ['id', 'passing_cmp', 'passing_att', 'passing_percent', 'passing_yards', 'passing_y/a', 'passing_td', 'passing_int',
              'sacks', 'rushing_att', 'rushing_yards', 'rushing_td', 'fumbles_lost', 'fantasy_points']
    data.columns = column
    data[['passing_cmp', 'passing_att', 'passing_yards', 'passing_td', 'passing_int', 'sacks', 'rushing_att', 'rushing_yards', 'rushing_td', 'fumbles_lost']] = data[['passing_cmp', 'passing_att', 'passing_yards', 'passing_td', 'passing_int', 'sacks', 'rushing_att', 'rushing_yards', 'rushing_td', 'fumbles_lost']].astype(int)
    data[['passing_percent', 'passing_y/a', 'fantasy_points']] = data[['passing_percent', 'passing_y/a', 'fantasy_points']].astype(float)
    data['total_td'] = data['passing_td'] + data['rushing_td']
    data['total_yards'] = data['passing_yards'] + data['rushing_yards']
    data['week'] = week

    return data


def skill_transform(data, week):
    # Transforms the raw skill position scraped table into formatted dataframe

    pass

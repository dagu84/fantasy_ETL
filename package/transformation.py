import pandas as pd

list = ['id', 'first_name', 'last_name', 'position', 'age', 'team', 'depth_chart_order', 'search_rank', 'active', 'college']

def player_table(data):
    df = pd.DataFrame(data)
    df = df.T
    df.reset_index(inplace=True)
    df.rename(columns={'index':'id'}, inplace=True)
    df = df[list]
    return df

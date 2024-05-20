import numpy as np
import pandas as pd

def player_transform(data):

    df = pd.DataFrame(data)
    df = df.T

    df.reset_index(inplace=True)
    df.rename(columns={'index':'id'}, inplace=True)
    df = df[['id', 'first_name', 'last_name', 'position', 'age', 'team', 'depth_chart_order', 'search_rank', 'college', 'years_exp', 'status']]

    df.replace('None', np.nan, inplace=True)
    df = df.infer_objects()

    return df

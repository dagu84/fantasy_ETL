import pandas as pd
import numpy as np

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

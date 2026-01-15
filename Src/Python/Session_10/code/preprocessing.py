import pandas as pd

def chek_type(data):
    dtypes = data.dtypes
    n_unique = data.nunique()
    return pd.DataFrame({ 'DataType': dtypes, 'NumUnique': n_unique}).T

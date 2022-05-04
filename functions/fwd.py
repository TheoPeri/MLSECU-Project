import pandas as pd

def delete_fwd(df):
    df.drop(columns = ["fwd"], axis =1, inplace=True)
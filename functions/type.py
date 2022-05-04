import pandas as pd

def delete_data_type(df):
    df.drop(columns = ["data_type"], axis =1, inplace=True)
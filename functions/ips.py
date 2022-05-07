import pandas as pd


def delete_ips(df):
    df.drop(columns = ["ip_d", "ip_s"], axis =1, inplace=True)
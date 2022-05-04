import pandas as pd


def generate_flag_columns(df):
    flags = ["U", "A", "P", "R", "S", "F"]

    df.flag.replace("\.", "0", regex=True, inplace=True)
    df.flag.replace("[^0]", "1", regex=True, inplace=True)

    for i in range(len(flags)):
        df["flag_" + flags[i]] = df.flag.str[i]

    df.drop(columns=["flag"], axis =1, inplace=True)
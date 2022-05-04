import pandas as pd

def convert_tos(df):
    df["tos_recedence"] = df.tos.apply(lambda x: int(format(int(x), '08b')[:3], 2))
    df["tos_delay"] = df.tos.apply(lambda x: int(format(int(x), '08b')[3]))
    df["tos_throughput"] = df.tos.apply(lambda x: int(format(int(x), '08b')[4]))
    df["tos_reliability"] = df.tos.apply(lambda x: int(format(int(x), '08b')[5]))
    df["tos_cost"] = df.tos.apply(lambda x: int(format(int(x), '08b')[6]))
    df["tos_congestion"] = df.tos.apply(lambda x: int(format(int(x), '08b')[7]))
    
    df.drop(columns = ["tos"], axis =1, inplace=True)
import pandas as pd


def generate_prot_encoding(df):
    famous_prots = ["TCP", "UDP", "ICMP", "GRE", "ESP", "IPIP", "IPv6"]
    
    for prot in famous_prots:
        df["prot_" + prot] = 0
        df.loc[df["prot"] == prot, "prot_" + prot] = 1
        
    df["prot_other"] = 1
    for prot in famous_prots:
        df.loc[df["prot_" + prot] == 1, "prot_other"] = 0
        
    df.drop(columns = ["prot"], axis =1, inplace=True)
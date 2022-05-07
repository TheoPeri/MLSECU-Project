import pandas as pd

def generate_port_type_columns(df):
    ports = pd.read_html("https://www.ionos.fr/digitalguide/serveur/know-how/ports-tcpet-udp/")
    port_use = pd.concat(ports).drop(["Nom", "Description"], axis=1)
    
    port_use.loc[port_use.TCP.isna() == False, "TCP"] = True
    port_use.loc[port_use.TCP.isna(), "TCP"] = False
    port_use.loc[port_use.UDP.isna() == False, "UDP"] = True
    port_use.loc[port_use.UDP.isna(), "UDP"] = False
    port_use.set_index('Port', inplace=True)

    ports_TCP_and_UDP = port_use[port_use.TCP & port_use.UDP].index.tolist()
    ports_TCP = port_use[port_use.TCP & (port_use.UDP == False)].index.tolist()
    ports_UDP = port_use[(port_use.TCP == False) & port_use.UDP].index.tolist()
    ports_not = port_use[(port_use.TCP == False) & (port_use.UDP == False)].index.tolist()
    
    df["port_d_TCP_UDP"] = 0
    df["port_d_TCP"] = 0
    df["port_d_UDP"] = 0
    df["port_d_not_TCP_UDP"] = 0
    df["port_d_unknown"] = 0
    
    df["port_s_TCP_UDP"] = 0
    df["port_s_TCP"] = 0
    df["port_s_UDP"] = 0
    df["port_s_not_TCP_UDP"] = 0
    df["port_s_unknown"] = 0
    
    df.loc[df["port_d"].isin(ports_TCP_and_UDP), "port_d_TCP_UDP"] = 1
    df.loc[df["port_d"].isin(ports_TCP), "port_d_TCP"] = 1
    df.loc[df["port_d"].isin(ports_UDP), "port_d_UDP"] = 1
    df.loc[df["port_d"].isin(ports_not), "port_d_not_TCP_UDP"] = 1
    df.loc[df["port_d_TCP_UDP"] + df["port_d_TCP"] + df["port_d_UDP"] + df["port_d_not_TCP_UDP"] == 0, "port_d_unknown"] = 1
    
    df.loc[df["port_s"].isin(ports_TCP_and_UDP), "port_s_TCP_UDP"] = 1
    df.loc[df["port_s"].isin(ports_TCP), "port_s_TCP"] = 1
    df.loc[df["port_s"].isin(ports_UDP), "port_s_UDP"] = 1
    df.loc[df["port_s"].isin(ports_not), "port_s_not_TCP_UDP"] = 1
    df.loc[df["port_s_TCP_UDP"] + df["port_s_TCP"] + df["port_s_UDP"] + df["port_s_not_TCP_UDP"] == 0, "port_s_unknown"] = 1

def split_port(df):
    df["port_s_system"] = -42
    df["port_s_registered"] = -42
    df["port_s_dynamic"] = -42
    
    df.loc[df["port_s"] < 1024, "port_s_system"] = df.loc[df["port_s"] < 1024, "port_s"]
    df.loc[(df["port_s"] >= 1024) & (df["port_s"] < 49152), "port_s_registered"] = df.loc[(df["port_s"] >= 1024) & (df["port_s"] < 49152), "port_s"] - 1024
    df.loc[df["port_s"] >= 49152, "port_s_dynamic"] = df.loc[df["port_s"] >= 49152, "port_s"] - 49152
    
    df["port_d_system"] = -42
    df["port_d_registered"] = -42
    df["port_d_dynamic"] = -42
    
    df.loc[df["port_d"] < 1024, "port_d_system"] = df.loc[df["port_d"] < 1024, "port_d"]
    df.loc[(df["port_d"] >= 1024) & (df["port_d"] < 49152), "port_d_registered"] = df.loc[(df["port_d"] >= 1024) & (df["port_d"] < 49152), "port_d"] - 1024
    df.loc[df["port_d"] >= 49152, "port_d_dynamic"] = df.loc[df["port_d"] >= 49152, "port_d"] - 49152
    
def remove_port(df):
    df.drop(columns = ["port_d", "port_s"], axis =1, inplace=True)
import pandas as pd
from zipfile import ZipFile
import os


class GetData(object):
    """
    we have 3 files.
    - data_base.zip - the file containing anomalies and normal traffic.
    - normal.zip - normal traffic
    - anomalies.zip - traffic presenting anomalies
    """

    def __init__(self):
        self.ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
        self.DATA_DIR = self.ROOT_DIR + "/data/"
        self.df_normal_traffic = self._get_df("normal")
        self.df_anomaly_traffic = self._get_df("anomalies")
        self.df_rounded_traffic = self._get_df("data_base")

    def get_flag_one_hot_encoding(self, df):
        flags = ["U", "A", "P", "R", "S", "F"]

        df.flag.replace("\.", "0", regex=True, inplace=True)
        df.flag.replace("[^0]", "1", regex=True, inplace=True)

        for i in range(len(flags)):
            df[flags[i]] = df.flag.str[i]

    def _get_df(self, file_base):
        self._unzipper(file_base)

        data_header = [
            "date_time",
            "duration",
            "ip_s",
            "ip_d",
            "port_s",
            "port_d",
            "prot",
            "flag",
            "fwd",
            "tos",
            "nb_packets",
            "nb_bytes",
            "data_type",
        ]

        path = self.DATA_DIR + "__use__/" + file_base + ".csv"

        return pd.read_csv(path, parse_dates=[0], index_col=[0], names=data_header)

    def _unzipper(self, file_path):
        path = self.DATA_DIR
        with ZipFile(path + file_path + ".zip", "r") as zipped_file:
            zipped_file.extractall(path + "__use__")

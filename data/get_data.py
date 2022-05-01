import pandas as pd
from zipfile import ZipFile


class GetData(object):
    """
    we have 3 files.
    - data_base.zip - the file containing anomalies and normal traffic.
    - normal.zip - normal traffic
    - anomalies.zip - traffic presenting anomalies
    """

    def __init__(self):
        self.df_normal_traffic = self._get_df("normal")
        self.df_anomaly_traffic = self._get_df("anomalies")
        self.df_rounded_traffic = self._get_df("data_base")

    def _get_df(self, file_base):
        self._unzipper(file_base)

        return pd.read_csv("__use__/" + file_base + ".csv")

    def _unzipper(self, file_path):
        with ZipFile(file_path + ".zip", "r") as zipped_file:
            zipped_file.extractall("__use__")

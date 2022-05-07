from functions.AI.AiAlgo import AiAlgo

from sklearn.neighbors import LocalOutlierFactor


class localOutlierFactor(AiAlgo):
    def __init__(self, df, outliers_fraction=0.267):
        self.b_df = df.copy()
        self.to_normalise = self._get_cols_to_normalise()
        self._normalise_cols()

        clf = LocalOutlierFactor(contamination=outliers_fraction)

        super().__init__(self.b_df, clf)

    def fit_and_score(self):
        algo_res = self.clf.fit_predict(self.X_valid)

        compare = self.X_valid.copy()
        compare["lof_outliers"] = algo_res
        compare["anomaly"] = self.y_valid

        correctly_identified = compare[
            (compare.anomaly == True) & (compare.lof_outliers == -1)
        ]

        num = correctly_identified.shape[0]
        den = compare.anomaly.shape[0]

        score = (num / den) * 100

        print("Score : {train:.2f}%".format(train=score))

    def _get_cols_to_normalise(self):
        to_normalise = []
        for col in self.b_df.columns:
            if self.b_df[col].dtype in ["int64", "float64"] and (
                self.b_df[col].max() > 1 or self.b_df[col].min() < -1
            ):
                to_normalise.append(col)

        return to_normalise

    def _min_max_normalisation(self, col):
        df_col = self.b_df[col]
        num = df_col - df_col.min()
        den = df_col.max() - df_col.min()

        return num / den

    def _normalise_cols(self):
        for col in self.to_normalise:
            self.b_df[col] = self._min_max_normalisation(col)

from functions.AI.AiAlgo import AiAlgo

import xgboost as xgb


class extremeGradientBoost(AiAlgo):
    def __init__(self, df, max_depth=2):
        self.b_df = df.copy()
        self._format_cols()

        clf = xgb.XGBClassifier(objective="binary:logistic", random_state=42)
        super().__init__(self.b_df, clf)

    def _format_cols(self):
        flag_cols = ["flag_U", "flag_A", "flag_P", "flag_R", "flag_S", "flag_F"]
        for col in flag_cols:
            self.b_df = self.b_df.astype({col: "int64"}, errors="raise")

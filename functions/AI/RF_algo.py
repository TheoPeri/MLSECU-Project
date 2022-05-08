from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from functions.AI.AiAlgo import AiAlgo


class randomForest(AiAlgo):
    def __init__(self, df, n_estimators=1):
        clf = RandomForestClassifier(
            n_estimators=n_estimators,
            random_state=0,
        )
        super().__init__(df, clf)

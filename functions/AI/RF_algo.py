from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from functions.AI.AiAlgo import AiAlgo


class randomForest(AiAlgo):
    def __init__(self, df, max_depth=2):
        clf = RandomForestClassifier(
            max_depth=max_depth,
            random_state=0,
        )
        super().__init__(df, clf)

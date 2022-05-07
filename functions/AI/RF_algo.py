from sklearn.ensemble import RandomForestClassifier


class randomForest(object):
    def __init__(self, df, max_depth=2):
        self.df = df

        self.X = self._get_X()
        self.y = self._get_y()

        self.clf = RandomForestClassifier(max_depth=max_depth, random_state=0)

    def get_sets(self):
        train_ratio = 0.70
        test_ratio = 0.20
        validation_ratio = 0.10

        X_train, X_test, y_train, y_test = train_test_split(
            self.X, self.y, test_size=test_ratio
        )

        X_train, X_valid, y_train, y_valid = train_test_split(
            X_train, y_train, test_size=validation_ratio / (train_ratio + test_ratio)
        )

        return X_train, X_test, X_valid, y_train, y_test, y_valid

    def algo(self, X_train, y_train):
        return clf.fit(X_train, y_train)

    def validation_score(self, X_valid, y_valid):
        return clf.score(X_valid, y_valid)

    def test_score(self, X_test, y_test):
        return clf.score(X_test, y_test)

    def _get_X(self):
        return self.df.copy().drop("anomaly", axis=1)

    def _get_y(self):
        return self.df.anomaly

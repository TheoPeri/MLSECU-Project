from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


class randomForest(object):
    def __init__(self, df, max_depth=2):
        self.df = df

        self.X = self._get_X()
        self.y = self._get_y()

        (
            self.X_train,
            self.X_test,
            self.X_valid,
            self.y_train,
            self.y_test,
            self.y_valid,
        ) = self.get_sets()

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

    def fit(self, X_train, y_train):
        return self.clf.fit(X_train, y_train)

    def score(self, X_data, y_data):
        return self.clf.score(X_data, y_data)

    def fit_and_score(self, validation=False):

        print(self.fit(self.X_train, self.y_train))

        train_score = self.score(self.X_train, self.y_train)
        test_score = self.score(self.X_test, self.y_test)

        print("Train Score     : {train:.2f}%".format(train=train_score * 100))
        print("Test Score      : {test:.2f}%".format(test=test_score * 100))

        if validation:
            validation_score = self.score(self.X_valid, self.y_valid)
            print(
                "Validation Score: {validation:.2f}%".format(
                    validation=validation_score * 100
                )
            )

    def _get_X(self):
        return self.df.copy().drop("anomaly", axis=1)

    def _get_y(self):
        return self.df.anomaly

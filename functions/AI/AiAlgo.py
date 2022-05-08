from sklearn.model_selection import train_test_split
from sklearn.model_selection import learning_curve
from sklearn.model_selection import validation_curve
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


class AiAlgo(object):
    def __init__(self, df, clf):
        self.df = df

        self.clf = clf

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

        self.graphs = self._renewGraphs()

    def _renewGraphs(self):
        self.graphs = AiAlgo.Graphs(self)

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

    def score_real(self, df):
        flag_cols = ["flag_U", "flag_A", "flag_P", "flag_R", "flag_S", "flag_F"]
        for col in flag_cols:
            df = df.astype({col: "int64"}, errors="raise")

        X, y = self._get_real_X(df), self._get_real_y(df)

        real_data_score = self.score(X, y)

        real_data_predict = self.clf.predict(X)

        compare = X.copy()
        compare["predicted"] = real_data_predict.copy()
        compare["anomaly"] = y.values

        print(
            "Percentage of anomaly in the dataset: {nb:.2f}%".format(
                nb=(y[y == True].shape[0] / y.shape[0]) * 100
            )
        )
        print(
            "Percentage of correctly identified anomalies {pct:.2f}%".format(
                pct=(
                    (
                        compare[
                            (compare["anomaly"] == True) & (compare["predicted"] == 1)
                        ].shape[0]
                        / compare[(compare["anomaly"] == True)].shape[0]
                    )
                    * 100
                )
            )
        )
        print(
            "Percentage of correctly identified normal traffic {pct:.2f}%".format(
                pct=(
                    (
                        compare[
                            (compare["anomaly"] == False) & (compare["predicted"] == 0)
                        ].shape[0]
                        / compare[(compare["anomaly"] == False)].shape[0]
                    )
                    * 100
                )
            )
        )
        print("Real Data Score : {real:.2f}%".format(real=real_data_score * 100))

    def fit_and_score(self, validation=False):
        evalset = [(self.X_train, self.y_train), (self.X_test, self.y_test)]
        print(self.clf.fit(self.X_train, self.y_train))

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

        self._renewGraphs()

    def _get_real_X(self, d):
        return d.copy().drop("anomaly", axis=1)

    def _get_real_y(self, d):
        return d.anomaly

    def _get_X(self):
        return self.df.copy().drop("anomaly", axis=1)

    def _get_y(self):
        return self.df.anomaly

    class Graphs:
        def __init__(self, outer):
            self.main = outer

        def feature_importance(self, dwld=False):
            estimator = self.main.clf

            feature_imp = pd.Series(
                self.main.clf.feature_importances_, index=self.main.X.columns.values
            ).sort_values(ascending=False)

            if dwld:
                plt.figure(figsize=(20, 12))
            else:
                plt.figure(figsize=(10, 6))

            sns.barplot(x=feature_imp, y=feature_imp.index)

            class_names = feature_imp.index

            tick_marks_y = np.arange(len(class_names))

            plt.xticks(rotation=0, fontsize=10)
            plt.yticks(tick_marks_y, class_names, rotation=25, fontsize=7)

            plt.xlabel("Feature Importance Score", fontsize=12)
            plt.ylabel("Features", fontsize=12)
            plt.title(
                "Visualizing Important Features for "
                + str(estimator).split("(")[0]
                + " model"
            )

            if dwld:
                plt.savefig(
                    str(estimator).split("(")[0] + "-featureImportance.svg",
                    format="svg",
                    dpi=1200,
                )

            plt.show()

        def confusion_matrix(self, dwld=False):
            estimator = self.main.clf
            y_pred_test = self.main.clf.predict(self.main.X_test)

            matrix = confusion_matrix(self.main.y_test, y_pred_test)
            matrix = matrix.astype("float") / matrix.sum(axis=1)[:, np.newaxis]

            if dwld:
                plt.figure(figsize=(16, 6))
            else:
                plt.figure(figsize=(8, 3))

            plt.rc("xtick", labelsize=10)
            plt.rc("ytick", labelsize=6)

            sns.set(font_scale=1.4)
            sns.heatmap(
                matrix,
                annot=True,
                annot_kws={"size": 10},
                cmap=plt.cm.Greens,
                linewidths=0.2,
            )

            class_names = ["Normal", "Anomaly"]

            tick_marks = np.arange(len(class_names)) + 0.5

            plt.xticks(tick_marks, class_names, rotation=0, fontsize=10)
            plt.yticks(tick_marks, class_names, rotation=90, fontsize=10)

            plt.xlabel("Predicted label", fontsize=12)
            plt.ylabel("True label", fontsize=12)

            plt.title("Confusion Matrix for " + str(estimator).split("(")[0] + " model")

            if dwld:
                plt.savefig(
                    str(estimator).split("(")[0] + "-confusionMatrix.svg",
                    format="svg",
                    dpi=1200,
                )
            plt.show()

        def model_accuracy_train_size(self):
            estimator = self.main.clf
            train_sizes, train_scores, test_scores = learning_curve(
                estimator=estimator,
                X=self.main.X,
                y=self.main.y,
                train_sizes=np.linspace(0.1, 1, 5),
                cv=5,
                n_jobs=-1,
            )

            train_mean = np.mean(train_scores, axis=1)
            train_std = np.std(train_scores, axis=1)
            test_mean = np.mean(test_scores, axis=1)
            test_std = np.std(test_scores, axis=1)

            plt.figure(figsize=(7, 7))
            plt.plot(
                train_sizes,
                train_mean,
                color="blue",
                marker="o",
                markersize=5,
                label="Training accuracy",
            )

            plt.fill_between(
                train_sizes,
                train_mean + train_std,
                train_mean - train_std,
                alpha=0.15,
                color="blue",
            )

            plt.plot(
                train_sizes,
                test_mean,
                color="red",
                linestyle="--",
                marker="s",
                markersize=5,
                label="Validation accuracy",
            )

            plt.fill_between(
                train_sizes,
                test_mean + test_std,
                test_mean - test_std,
                alpha=0.15,
                color="green",
            )

            plt.grid(visible=True)
            plt.xlabel("Number of training examples", fontsize=14)
            plt.ylabel("Model Accuracy", fontsize=14)

            title = (
                "Accuracy in relation to number of training examples for a "
                + str(estimator).split("(")[0]
                + " model"
            )
            plt.title(title, fontsize=18, y=1.03)
            plt.legend(loc="best")
            plt.show

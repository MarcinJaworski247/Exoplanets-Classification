from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import pandas as pd
from sklearn.tree import export_graphviz
import os


def classify(df):
    # class variable
    Y = df.koi_disposition.values
    Y = Y.astype('int')

    # independent variables
    X = df.drop(labels=['koi_disposition'], axis=1)

    # split data into train and test datasets
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.4, random_state=20)

    model = RandomForestClassifier(n_estimators=10)

    model.fit(X_train, Y_train)

    prediction_test = model.predict(X_test)

    # show model accuracy
    print("Accuracy = ", metrics.accuracy_score(Y_test, prediction_test))

    # f1 metric
    print("F1 score = ", metrics.f1_score(Y_test, prediction_test))

    # balanced accuracy score
    print("Balanced accuracy score = ",
          metrics.balanced_accuracy_score(Y_test, prediction_test))

    # top k accuracy score
    # print("Top K accuracy score = ",
    #       metrics.top_k_accuracy_score(Y_test, prediction_test))

    # brier_score_loss
    print("Brier score loss = ", metrics.brier_score_loss(Y_test, prediction_test))

    # average_precision_score
    print("Average precision score = ",
          metrics.average_precision_score(Y_test, prediction_test))

    feature_list = list(X.columns)
    feature_imp = pd.Series(model.feature_importances_,
                            index=feature_list).sort_values(ascending=False)

    # show variables importance
    print(feature_imp)

    # visualize trees
    feature_names = X.columns
    class_name = 'koi_disposition'
    for i in range(0, len(model.estimators_)):
        visualizeTree(model.estimators_[i], i, feature_names, class_name)


def visualizeTree(estimator, number, featurenames, classname):
    print(f"tree-{number}.dot")
    # export as dot file
    export_graphviz(estimator, out_file=f"tree-{number}.dot", feature_names=featurenames,
                    class_names=classname, rounded=True, proportion=False, precision=2, filled=True)
    os.system(f'dot -Tpng tree-{number}.dot -o tree-{number}.png')

from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


# def showCorrelation(col_x, col_y):
#     sns.regplot(x=col_x, y=col_y)
#     plt.show()

# Each variable histograms


def showHistograms(df):
    df.hist(density=True)
    plt.title("Variables histogram")
    plt.show()


# Specific column boxplot
def showBoxplot(df, col):
    df[col].plot(kind="box")
    plt.title(f"{str(col)} variable boxplot")
    plt.show()

# Each variable boxplot


def showAllBoxplots(df):
    df.boxplot()
    plt.show()

# Pearson linear regression heatmap


def showPearsonRegression(df):
    correlations = df.corr()
    sns.heatmap(correlations, annot=True,
                cmap="Greens", annot_kws={"size": 8}, vmin=-1, vmax=1)
    plt.title("Pearson Correlation Matrix")
    plt.show()

# Pearson linear regression between variables and class heatmap


def showPearsonRegressionWithClass(class_corr_dict):
    for col in class_corr_dict:
        class_corr_dict[col] = [round(class_corr_dict[col], 4)]
    df = pd.DataFrame.from_dict(class_corr_dict)

    sns.heatmap(df, annot=True, fmt="g", cmap="Greens")
    plt.title("Pearson Correlation With Class")
    plt.show()

# Simple linear regression between two columns and scatterplot (wykres rozrzutu)


def showSimpleLinearRegression(col_x, col_y):
    x = np.array(col_x).reshape((-1, 1))
    y = np.array(col_y).reshape((-1, 1))
    model = LinearRegression()
    model.fit(x, y)
    y_pred = model.predict(x)
    plt.scatter(x, y, color="red")
    plt.plot(x, y_pred, color="green")
    plt.show()

# Variables values


def showValuesTight(df):
    df.plot(subplots=True)
    plt.tight_layout()
    plt.show()


def showValuesLayout(df):
    df.plot(subplots=True, layout=(5, 3))
    plt.show()

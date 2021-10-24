from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np


def showCorrelation(col_x, col_y):
    sns.regplot(x=col_x, y=col_y)
    plt.show()


def showLinearRegression(x, y, y_pred):
    plt.scatter(x, y, color="red")
    plt.plot(x, y_pred, color="green")
    plt.show()


def showHistogram(col):

    q25, q75 = np.percentile(col, [0.25, 0.75])
    bin_width = 2 * (q75 - q25) * len(col) ** (-1/3)
    bins = int((col.max() - col.min()) / bin_width)
    print(bins)
    plt.hist(col, bins=bins)
    plt.show()


def showBoxplot(col):
    fig = plt.figure(figsize=(10, 7))
    plt.boxplot(col)
    plt.show()

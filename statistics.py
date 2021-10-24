import numpy as np
from sklearn.linear_model import LinearRegression
import plots as plots


def getRanges(data):
    ranges = {}
    for col in data.columns:
        ranges.update({col: [data[col].min, data[col].max]})
    return ranges


def getAverages(data):
    averages = {}
    for col in data.columns:
        averages.update({col: data[col].mean()})
    return averages


def getStandardDeviations(data):
    standard_deviations = {}
    for col in data.columns:
        standard_deviations.update({col: data[col].std()})
    return standard_deviations


def getMedians(data):
    medians = {}
    for col in data.columns:
        medians.update({col: data[col].median()})
    return medians


def calculateInterquartileRanges(data, col):
    Q3 = np.quantile(data[col], 0.75)
    Q1 = np.quantile(data[col], 0.25)
    return Q3 - Q1


def getInterquartileRanges(data):
    iqr = {}
    for col in data.columns:
        iqr.update({col: calculateInterquartileRanges(data, col)})
    return iqr


def getQuantiles(data, range):
    result = {}
    for col in data.columns:
        result.update({col: np.quantile(data[col], range)})


def detectOutliers(data, col):
    Q3 = np.quantile(data[col], 0.75)
    Q1 = np.quantile(data[col], 0.25)
    IQR = Q3 - Q1
    lower_range = Q1 - 1.5 * IQR
    upper_range = Q3 + 1.5 * IQR

    global outliers

    outlier_list = [x for x in data[col] if (
        (x < lower_range) & (x > upper_range)
    )]
    outliers = data.loc[data[col].isin(outlier_list)]
    # if (len(outliers.head())):
    #     print("There are outliers in data")
    # else:
    #     print("There are no outliers")


def simpleLinearRegression(col_x, col_y):
    x = np.array(col_x).reshape((-1, 1))
    y = np.array(col_y).reshape((-1, 1))
    model = LinearRegression()
    model.fit(x, y)
    y_pred = model.predict(x)
    r_sq = model.score(x, y)
    # plots.showLinearRegression(x, y, y_pred)
    return r_sq


def findPearsonLinearCorrelation(statistic_data):
    for col_x in statistic_data.columns:
        for col_y in statistic_data.columns:
            if col_x != col_y:
                corr = statistic_data[col_x].corr(statistic_data[col_y])
                # if abs(corr) > 0.6:
                # print(
                #     f"Moderate correlation ({corr}) between {col_x} and {col_y}")
                # plots.showCorrelation(
                #     statistic_data[col_x], statistic_data[col_y])


def findPearsonLinearCorrelationWithClass(statistics_data, class_var):
    correlations = {}
    for col in statistics_data.columns:
        corr = np.corrcoef(class_var.astype(
            float), statistics_data[col].astype(float))
        correlations.update({col: abs(corr[0][1])})

    # highest correlation
    # for col in correlations:
    #     print(col + " - " + str(correlations[col]))

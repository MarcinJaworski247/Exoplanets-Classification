import numpy as np
from sklearn.linear_model import LinearRegression


def getRanges(data):
    ranges = {}
    for col in data.columns:
        ranges.update({col: [data[col].min(), data[col].max()]})
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
    return result


def detectOutliers(columns):
    counter = 0
    for col in columns:
        data = columns[col]
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        lower_range = Q1 - 1.5 * IQR
        upper_range = Q3 + 1.5 * IQR

        name = col
        for val in data:
            if val < lower_range or val > upper_range:
                print(f"Attribute: {name}, Value: {val}")
                counter = counter + 1
        print(f"Amount of outliers: {counter}")


def findPearsonLinearCorrelation(statistic_data):
    return statistic_data.corr(method="pearson")


def findPearsonLinearCorrelationWithClass(statistics_data, class_var):
    correlations = {}
    for col in statistics_data.columns:
        corr = np.corrcoef(class_var.astype(
            float), statistics_data[col].astype(float))
        correlations.update({col: abs(corr[0][1])})
    return correlations


def simpleLinearRegression(col_x, col_y):
    x = np.array(col_x).reshape((-1, 1))
    y = np.array(col_y).reshape((-1, 1))
    model = LinearRegression()
    model.fit(x, y)
    r_sq = model.score(x, y)
    return r_sq

import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from random import randrange

import data_preparation as data_prep
import statistics as stats


# csv file name
file_name = "cumulative_2021.10.09_13.05.19.csv"

# read data from csv. skip first 31 rows which are just in informative purpose
df = pd.read_csv(file_name, skiprows=31)

# drop not nesessary columns
df = data_prep.dropNotNessesaryColumns(df)

# convert CONFIRMED and FALSE POSITIVE to 1 and 0
# df.koi_disposition[df.koi_disposition == "CONFIRMED"] = 1
# df.koi_disposition[df.koi_disposition == "FALSE POSITIVE"] = 0

# delete CANDIDATES
df = data_prep.deleteCandidates(df)

# check if some column have more than 50% empty cells. if so delete it
# print(df.isna().sum())
# df = df.loc[:, df.isin([None, 'NULL', 0]).mean() < .5]

# fill empty cells
df = data_prep.fillEmptyCells(df)


statistic_data = data_prep.getStatisticsColumns(df)

# min - max


ranges = stats.getRanges(statistic_data)

# averages


averages = stats.getAverages(statistic_data)

# standard deviation


standard_deviations = stats.getStandardDeviations(statistic_data)

# median of variables


medians = stats.getMedians(statistic_data)


# interquartile ranges for variables - IQR = Q3 - Q1


interquartile_ranges = stats.getInterquartileRanges(statistic_data)


# quantile 0.1


quantiles_01 = stats.getQuantiles(statistic_data, 0.1)

# quantile 0.9

quantiles_09 = stats.getQuantiles(statistic_data, 0.9)

# outliers detection


for col in statistic_data.columns:
    stats.detectOutliers(statistic_data, col)


# Pearson linear correlation between columns
all_cols_corr = statistic_data.corr()

import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from random import randrange

# csv file name
file_name = "cumulative_2021.10.09_13.05.19.csv"

# read data from csv. skip first 31 rows which are just in informative purpose
df = pd.read_csv(file_name, skiprows=31)

# drop not nesessary columns
df.drop(["loc_rowid", "kepid", "koi_pdisposition", "koi_score",
        "koi_tce_plnt_num", "koi_tce_delivname"], axis=1, inplace=True)

# convert CONFIRMED and FALSE POSITIVE to 1 and 0
# df.koi_disposition[df.koi_disposition == "CONFIRMED"] = 1
# df.koi_disposition[df.koi_disposition == "FALSE POSITIVE"] = 0

# delete CANDIDATES
df = df[df.koi_disposition != "CANDIDATE"]

# check if some column have more than 50% empty cells. if so delete it
# print(df.isna().sum())
# df = df.loc[:, df.isin([None, 'NULL', 0]).mean() < .5]

# fill empty cells
df.koi_fpflag_nt.fillna(randrange(1), inplace=True)
df.koi_fpflag_co.fillna(randrange(1), inplace=True)
df.koi_fpflag_ec.fillna(randrange(1), inplace=True)
df.koi_fpflag_nt.fillna(randrange(1), inplace=True)
df.koi_period.fillna(df.koi_period.mean(), inplace=True)
df.koi_time0bk.fillna(df.koi_time0bk.mean(), inplace=True)
df.koi_impact.fillna(df.koi_impact.mean(), inplace=True)
df.koi_duration.fillna(df.koi_duration.mean(), inplace=True)
df.koi_depth.fillna(df.koi_depth.mean(), inplace=True)
df.koi_prad.fillna(df.koi_prad.mean(), inplace=True)
df.koi_teq.fillna(df.koi_teq.mean(), inplace=True)
df.koi_insol.fillna(df.koi_insol.mean(), inplace=True)
df.koi_model_snr.fillna(df.koi_model_snr.mean(), inplace=True)
df.koi_steff.fillna(df.koi_steff.mean(), inplace=True)
df.koi_slogg.fillna(df.koi_slogg.mean(), inplace=True)
df.koi_srad.fillna(df.koi_srad.mean(), inplace=True)
df.ra.fillna(df.ra.mean(), inplace=True)
df.dec.fillna(df.dec.mean(), inplace=True)
df.koi_kepmag.fillna(df.koi_kepmag.mean(), inplace=True)

statistic_columns = [
    "koi_period",
    "koi_time0bk",
    "koi_impact",
    "koi_duration",
    "koi_depth",
    "koi_prad",
    "koi_teq",
    "koi_insol",
    "koi_model_snr",
    "koi_steff",
    "koi_slogg",
    "koi_srad",
    "ra",
    "dec",
    "koi_kepmag"
]

# min - max

ranges = {}
for col in statistic_columns:
    ranges.update({col: [df[col].min, df[col].max]})

# averages

averages = {}
for col in statistic_columns:
    averages.update({col: df[col].mean()})

# standard deviation

standard_deviations = {}
for col in statistic_columns:
    standard_deviations.update({col: df[col].std()})

# median of variables

medians = {}
for col in statistic_columns:
    medians.update({col: df[col].median()})

# interquartile ranges for variables - IQR = Q3 - Q1


def calculateInterquartileRanges(col):
    Q3 = np.quantile(df[col], 0.75)
    Q1 = np.quantile(df[col], 0.25)
    return Q3 - Q1


iqr = {}
for col in statistic_columns:
    iqr.update({col: calculateInterquartileRanges(col)})

# quantile 0.1

quantiles_01 = {}

for col in statistic_columns:
    quantiles_01.update({col: np.quantile(df[col], 0.1)})

# quantile 0.9

quantiles_09 = {}

for col in statistic_columns:
    quantiles_09.update({col: np.quantile(df[col], 0.9)})

# outliers detection TO DO FIX !!!!


def detectOutliers(col):
    Q3 = np.quantile(df[col], 0.75)
    Q1 = np.quantile(df[col], 0.25)
    IQR = Q3 - Q1
    lower_range = Q1 - 1.5 * IQR
    upper_range = Q3 + 1.5 * IQR

    global outliers

    outlier_list = [x for x in df[col] if (
        (x < lower_range) & (x > upper_range)
    )]
    outliers = df.loc[df[col].isin(outlier_list)]


for col in statistic_columns:
    detectOutliers(col)

# print(outliers.head())

# Pearson linear correlation between two columns

# example
example_correlation = df.koi_period.corr(df.koi_duration)
print(example_correlation)

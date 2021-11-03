import pandas as pd
import data_preparation as data_prep
import statistics as stats
import plots
import file_operations as fp

# ---------------------------- DATA PREPARATION --------------------------------------------

# csv file name
file_name = "cumulative_2021.10.09_13.05.19.csv"

# read data from csv. skip first 31 rows which are just in informative purpose
df = pd.read_csv(file_name, skiprows=31)

# drop not nesessary columns
df = data_prep.dropNotNessesaryColumns(df)

# convert CONFIRMED and FALSE POSITIVE to 1 and 0
df.koi_disposition.loc[(df.koi_disposition == "CONFIRMED")] = 1
df.koi_disposition.loc[(df.koi_disposition == "FALSE POSITIVE")] = 0

# delete CANDIDATES
df = data_prep.deleteCandidates(df)

# get class column to separate dataframe
class_column = data_prep.getClassColumn(df)

# check if some column have more than 50% empty cells. if so delete it
# df = df.loc[:, df.isin([None, 'NULL', 0]).mean() < .5]

# fill empty cells
df = data_prep.fillEmptyCells(df)

# get statistic columns to seperate dataframe
statistic_data = data_prep.getStatisticsColumns(df)


# outliers detection
# outl = stats.detectOutliers(statistic_data)

# save prepared data to csv file
fp.savePreparedData(df, "prepared_data")


# ---------------------------- STATISTICAL ANALYSIS ----------------------------------------


# min - max

ranges = stats.getRanges(statistic_data)

fp.saveRanges(ranges, "values_ranges.csv")

# averages

averages = stats.getAverages(statistic_data)
fp.saveDictionary(averages, "averages.csv", "Avg")

# standard deviation

standard_deviations = stats.getStandardDeviations(statistic_data)
fp.saveDictionary(standard_deviations, "standard_deviations.csv", "Stdv")

# median of variables

medians = stats.getMedians(statistic_data)
fp.saveDictionary(medians, "medians.csv", "Median")

# interquartile ranges for variables - IQR = Q3 - Q1

interquartile_ranges = stats.getInterquartileRanges(statistic_data)
fp.saveDictionary(interquartile_ranges, "iqr.csv", "IQR")

# quantile 0.1

quantiles_01 = stats.getQuantiles(statistic_data, 0.1)
fp.saveDictionary(quantiles_01, "quantile_0_1.csv", "Quantile 0.1")

# quantile 0.9

quantiles_09 = stats.getQuantiles(statistic_data, 0.9)
fp.saveDictionary(quantiles_09, "quantile_0_9.csv", "Quantile 0.9")

# Pearson linear correlation between columns
corr = stats.findPearsonLinearCorrelation(statistic_data)
fp.saveDataFrame(corr, "pearson_correlation_between_columns.csv")

# Pearson linear correlation between variables and class
class_corr = stats.findPearsonLinearCorrelationWithClass(
    statistic_data, class_column)
fp.saveDictionary(class_corr, "pearson_correlation_with_class.csv",
                  "Pearson linear correlation")


# simple linear regression between two columns
# koi_prad - koi_impact
r_sq_1 = stats.simpleLinearRegression(
    statistic_data.koi_prad, statistic_data.koi_impact)
print(f"Regression score between [koi_prad] and [koi_impact]: {r_sq_1}")
# koi_time0bk - koi_period
r_sq_2 = stats.simpleLinearRegression(
    statistic_data.koi_time0bk, statistic_data.koi_period)
print(f"Regression score between [koi_time0bk] and [koi_period]: {r_sq_2}")
# koi_insol - koi_srad
r_sq_3 = stats.simpleLinearRegression(
    statistic_data.koi_insol, statistic_data.koi_srad)
print(f"Regression score between [koi_insol] and [koi_srad]: {r_sq_3}")
# koi_teq - koi_disposition
r_sq_4 = stats.simpleLinearRegression(
    statistic_data.koi_teq, class_column)
print(
    f"Regression score between [koi_koi_teqinsol] and [koi_disposition]: {r_sq_4}")

# ---------------------------- DATA VISUALIZING --------------------------------------------

# Variables values
# plots.showValuesTight(statistic_data)
# plots.showValuesLayout(statistic_data)

# # histograms
# plots.showHistograms(statistic_data)

# # Pearson Linear Correlation
# plots.showPearsonRegressionWithClass(class_corr)
# plots.showPearsonRegression(statistic_data)

# boxplot
plots.showBoxplot(statistic_data, "ra")
plots.showBoxplot(statistic_data, "koi_kepmag")
plots.showBoxplot(statistic_data, "koi_steff")

# Simple linear regression with scatterplot
# koi_prad - koi_impact
# plots.showSimpleLinearRegression(
#     statistic_data.koi_prad, statistic_data.koi_impact)
# # koi_time0bk - koi_period
# plots.showSimpleLinearRegression(
#     statistic_data.koi_time0bk, statistic_data.koi_period)
# # koi_insol - koi_srad
# plots.showSimpleLinearRegression(
#     statistic_data.koi_insol, statistic_data.koi_srad)
# # koi_teq - koi_disposition
# plots.showSimpleLinearRegression(
#     statistic_data.koi_teq, class_column)

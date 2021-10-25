import csv


def savePreparedData(data_frame, name):
    data_frame.to_csv(name + ".csv", index=False)


def saveRanges(data_frame, name):
    with open(name, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(["Column", "Min", "Max"])
        for col in data_frame:
            writer.writerow([col, data_frame[col][0], data_frame[col][1]])


def saveDictionary(data_frame, name, col_name):
    with open(name, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(["Column", col_name])
        for col in data_frame:
            writer.writerow([col, data_frame[col]])


def saveDataFrame(df, name,):
    df.to_csv(name, sep=",")

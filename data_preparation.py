from random import randrange


def fillEmptyCells(df):
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
    return df


def getClassColumn(df):
    return df.koi_disposition


def dropNotNessesaryColumns(df):
    df.drop(["loc_rowid", "kepid", "koi_pdisposition", "koi_score",
             "koi_tce_plnt_num", "koi_tce_delivname"], axis=1, inplace=True)
    return df


def deleteCandidates(df):
    df = df[df.koi_disposition != "CANDIDATE"]
    return df


def getStatisticsColumns(df):
    df.drop(["koi_fpflag_nt", "koi_fpflag_co", "koi_fpflag_ec",
            "koi_fpflag_nt", "kepoi_name", "kepler_name", "koi_disposition"], axis=1, inplace=True)
    return df

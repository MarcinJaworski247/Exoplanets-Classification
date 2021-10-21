import csv
from itertools import islice
import random
from random import randrange
import statistics

# --------------------- DATA PREPARATION ---------------------------------
title = ""
date = ""
column_descriptions = []
# dictionaries list of read data
detected_objects = []

file_name = "cumulative_2021.10.09_13.05.19.csv"

# get title and generation date of a csv data file
with open(file_name, newline="") as csvdata:
    base_reader = csv.reader(csvdata)
    title = str(next(base_reader))
    date = str(next(base_reader))

# title and date cleanup
# remove first 4 characters from string
title = title[4:]
# remove last 2 characters from string
title = title[:-2]

date = date[4:]
date = date[:-2]

# read column names descriptions
with open(file_name, newline="") as csvdata:
    base_reader = csv.reader(islice(csvdata, 4, 30))
    for row in base_reader:
        column_descriptions.append(row)

# prepare column descriptions strings
for idx in range(len(column_descriptions)):
    column_descriptions[idx] = str(column_descriptions[idx]).split(":", 1)[1]
    column_descriptions[idx] = str(column_descriptions[idx][:-2])
    column_descriptions[idx] = str(column_descriptions[idx]).lstrip()

# delete not nessesary column names
clean = [i for i in column_descriptions if not(i == "Disposition Using Kepler Data" or i == "Disposition Score" or i == "TCE Planet Number" or i == "TCE Delivery")]
column_descriptions.clear()
column_descriptions = clean

# read data and map to dictionaries
with open(file_name, newline="") as csvdata:
    dict_reader = csv.DictReader(islice(csvdata, 31, None))
    for line in dict_reader:
        detected_objects.append(line)

# delete not nessesary columns
for idx in range(len(detected_objects)):
    for dict in list(detected_objects[idx]):
        if dict == "loc_rowid" or dict == "kepid" or dict == "koi_pdisposition" or dict == "koi_score" or dict == "koi_tce_plnt_num" or dict == "koi_tce_delivname":
            del detected_objects[idx][str(dict)]

# change "CONFIRMED" to True and "FALSE POSITIVE" to False - koi_disposition column
for obj in detected_objects:
    if obj["koi_disposition"] == "CONFIRMED":
        obj["koi_disposition"] = True
    elif obj["koi_disposition"] == "FALSE POSITIVE":
        obj["koi_disposition"] = False

# delete rows where koi_disposition is not "CONFIRMED" or "FALSE POSITIVE"
clean = [i for i in detected_objects if not(i["koi_disposition"] == "CANDIDATE" or i["koi_disposition"] == "NOT DISPOSITIONED")]
detected_objects.clear()
detected_objects = clean

# change dictionaries keys to these from column_descriptions list
for idx in range(len(detected_objects)):
    i = 0
    for dict in list(detected_objects[idx]):
        detected_objects[idx][column_descriptions[i]] = detected_objects[idx][str(dict)]
        del detected_objects[idx][str(dict)]            
        i += 1
    i = 0


# write prepared data to csv file
# keys = detected_objects[0].keys()
# with open("test.csv", "w", newline="") as prepared_data:
#     writer = csv.DictWriter(prepared_data, keys)
#     writer.writeheader()
#     writer.writerows(detected_objects)


# --------------------- STATISTICAL ANALYSE ---------------------------------

# not_statistic_columns = [
#     "KOI Name", 
#     "Kepler Name", 
#     "Exoplanet Archive Disposition", 
#     "Not Transit-Like False Positive Flag", 
#     "Stellar Eclipse False Positive Flag", 
#     "Centroid Offset False Positive Flag", 
#     "Ephemeris Match Indicates Contamination False Positive Flag"
# ]

# Averages including empty cell values
orbital_period_avg = 0
transit_epoch_avg = 0
impact_parameter_avg = 0
transit_duration_avg = 0
transit_depth_avg = 0
planetary_radius_avg = 0
equilibrium_temperature_avg = 0
insolation_flux_avg = 0
transit_signal_to_noise_avg = 0
stellar_effective_temperature_avg = 0
stellar_surface_gravity_avg = 0
stellar_radius_avg = 0
ra_avg = 0
dec_avg = 0
kepler_band_avg = 0

rows_count = len(detected_objects)

for obj in detected_objects:
    for col in obj:
        if col == "Orbital Period [days]" and obj.get(col) is not None and obj.get(col) != "":
            orbital_period_avg = orbital_period_avg + float(obj.get(col))
        if col == "Transit Epoch [BKJD]" and obj.get(col) is not None and obj.get(col) != "":
            transit_epoch_avg = transit_epoch_avg + float(obj.get(col))
        if col == "Impact Parameter" and obj.get(col) is not None and obj.get(col) != "":
            impact_parameter_avg = impact_parameter_avg + float(obj.get(col))
        if col == "Transit Duration [hrs]" and obj.get(col) is not None and obj.get(col) != "":
            transit_duration_avg = transit_duration_avg + float(obj.get(col))
        if col == "Transit Depth [ppm]" and obj.get(col) is not None and obj.get(col) != "":
            transit_depth_avg = transit_depth_avg + float(obj.get(col))
        if col == "Planetary Radius [Earth radii]" and obj.get(col) is not None and obj.get(col) !="":
            planetary_radius_avg = planetary_radius_avg + float(obj.get(col))
        if col == "Equilibrium Temperature [K]" and obj.get(col) is not None and obj.get(col) !="":
            equilibrium_temperature_avg = equilibrium_temperature_avg + float(obj.get(col))
        if col == "Insolation Flux [Earth flux]" and obj.get(col) is not None and obj.get(col) != "":
            insolation_flux_avg = insolation_flux_avg + float(obj.get(col))
        if col == "Transit Signal-to-Noise" and obj.get(col) is not None and obj.get(col) != "":
            transit_signal_to_noise_avg = transit_signal_to_noise_avg + float(obj.get(col))
        if col == "Stellar Effective Temperature [K]" and obj.get(col) is not None and obj.get(col) !="":
            stellar_effective_temperature_avg = stellar_effective_temperature_avg + float(obj.get(col))
        if col == "Stellar Surface Gravity [log10(cm/s**2)]" and obj.get(col) is not None and obj.get(col) != "":
            stellar_surface_gravity_avg = stellar_surface_gravity_avg + float(obj.get(col))
        if col == "Stellar Radius [Solar radii]" and obj.get(col) is not None and obj.get(col) != "":
            stellar_radius_avg = stellar_radius_avg + float(obj.get(col))
        if col == "RA [decimal degrees]" and obj.get(col) is not None and obj.get(col) != "":
            ra_avg = ra_avg + float(obj.get(col))
        if col == "Dec [decimal degrees]" and obj.get(col) is not None and obj.get(col) != "":
            dec_avg = dec_avg + float(obj.get(col))
        if col == "Kepler-band [mag]" and obj.get(col) is not None and obj.get(col) != "":
            kepler_band_avg = kepler_band_avg + float(obj.get(col))

orbital_period_avg = orbital_period_avg / rows_count
transit_depth_avg = transit_depth_avg / rows_count
impact_parameter_avg = impact_parameter_avg / rows_count
transit_duration_avg = transit_duration_avg / rows_count
transit_depth_avg = transit_depth_avg / rows_count
planetary_radius_avg = planetary_radius_avg / rows_count
equilibrium_temperature_avg = equilibrium_temperature_avg / rows_count
insolation_flux_avg = insolation_flux_avg / rows_count
transit_signal_to_noise_avg = transit_signal_to_noise_avg / rows_count
stellar_effective_temperature_avg = stellar_effective_temperature_avg / rows_count
stellar_surface_gravity_avg = stellar_surface_gravity_avg / rows_count
ra_avg = ra_avg / rows_count
dec_avg = dec_avg / rows_count
kepler_band_avg = kepler_band_avg / rows_count


# check if every value exists. if not assign avarage value or a random value if a column holds 0 or 1
for obj in detected_objects:
    for col in obj:
        if obj.get(col) is None or obj.get(col) == "":
            
            if col == "Exoplanet Archive Disposition":
                obj[col] = bool(random.getrandbits(1))
            if col == "Not Transit-Like False Positive Flag":
                obj[col] = randrange(1)
            if col == "Stellar Eclipse Flag":
                obj[col] = randrange(1)
            if col == "Centroid Offset Flag":
                obj[col] = randrange(1)
            if col == "Ephemeris Match Indicates Contamination Flag":
                obj[col] = randrange(1)
            if col == "Orbital Period [days]":
                obj[col] = orbital_period_avg
            if col == "Transit Epoch [BKJD]":
                obj[col] = transit_epoch_avg
            if col == "Impact Parameter":
                obj[col] = impact_parameter_avg
            if col == "Transit Duration [hrs]" :
                obj[col] = transit_duration_avg
            if col == "Transit Depth [ppm]":
                obj[col] = transit_depth_avg

            if col == "Planetary Radius [Earth radii]":
                obj[col] = planetary_radius_avg
            if col == "Equilibrium Temperature [K]":
                obj[col] = equilibrium_temperature_avg
            if col == "Insolation Flux [Earth flux]":
                obj[col] = insolation_flux_avg
            if col == "Transit Signal-to-Noise" :
                obj[col] = transit_signal_to_noise_avg
            if col == "Stellar Effective Temperature [K]":
                obj[col] = stellar_effective_temperature_avg
            if col == "Stellar Surface Gravity [log10(cm/s**2)]":
                obj[col] = stellar_surface_gravity_avg
            if col == "Stellar Radius [Solar radii]":
                obj[col] = stellar_radius_avg
            if col == "RA [decimal degrees]":
                obj[col] = ra_avg
            if col == "Dec [decimal degrees]":
                obj[col] = dec_avg
            if col == "Kepler-band [mag]":
                obj[col] = kepler_band_avg

# MIN - MAX

# Orbital Period [days]
orbital_days_col = "Orbital Period [days]"
orbital_days_min = float(detected_objects[0].get(orbital_days_col))
orbital_days_max = 0
# Transit Epoch [BKJD]
transit_epoch_col = "Transit Epoch [BKJD]"
transit_epoch_min = float(detected_objects[0].get(transit_epoch_col))
transit_epoch_max = 0
# Impact Parameter
impact_parameter_col = "Impact Parameter"
impact_parameter_min = float(detected_objects[0].get(impact_parameter_col))
impact_parameter_max = 0
# Transit Duration [hrs]
transit_duration_col = "Transit Duration [hrs]"
transit_duration_min = float(detected_objects[0].get(transit_duration_col))
transit_duration_max = 0
# Transit Depth [ppm]
transit_depth_col = "Transit Depth [ppm]"
transit_depth_min = float(detected_objects[0].get(transit_depth_col))
transit_depth_max = 0
# Planetary Radius [Earth radii]
planetary_radius_col = "Planetary Radius [Earth radii]"
planetary_radius_min = float(detected_objects[0].get(planetary_radius_col))
planetary_radius_max = 0
# Equilibrium Temperature [K]
equilibrium_temperature_col = "Equilibrium Temperature [K]"
equilibrium_temperature_min = float(detected_objects[0].get(equilibrium_temperature_col))
equilibrium_temperature_max = 0
# Insolation Flux [Earth flux]
insolation_flux_col = "Insolation Flux [Earth flux]"
insolation_flux_min = float(detected_objects[0].get(insolation_flux_col))
insolation_flux_max = 0
# Transit Signal-to-Noise
transit_signal_to_noise_col = "Transit Signal-to-Noise"
transit_signal_to_noise_min = float(detected_objects[0].get(transit_signal_to_noise_col))
transit_signal_to_noise_max = 0
# Stellar Effective Temperature [K]
stellar_effective_temperature_col = "Stellar Effective Temperature [K]"
stellar_effective_temperature_min = float(detected_objects[0].get(stellar_effective_temperature_col))
stellar_effective_temperature_max = 0
# Stellar Surface Gravity [log10(cm/s**2)]
stellar_surface_gravity_col = "Stellar Surface Gravity [log10(cm/s**2)]"
stellar_surface_gravity_min = float(detected_objects[0].get(stellar_surface_gravity_col))
stellar_surface_gravity_max = 0
# Stellar Radius [Solar radii]
stellar_radius_col = "Stellar Radius [Solar radii]"
stellar_radius_min = float(detected_objects[0].get(stellar_radius_col))
stellar_radius_max = 0
# RA [decimal degrees]
ra_col = "RA [decimal degrees]"
ra_min = float(detected_objects[0].get(ra_col))
ra_max = 0
# Dec [decimal degrees]
dec_col = "Dec [decimal degrees]"
dec_min = float(detected_objects[0].get(dec_col))
dec_max = 0
# Kepler-band [mag]
kepler_band_col = "Kepler-band [mag]"
kepler_band_min = float(detected_objects[0].get(kepler_band_col))
kepler_band_max = 0

for obj in detected_objects:
    # Orbital Period [days]
    if float(obj.get(orbital_days_col)) > orbital_days_max:
        orbital_days_max = float(obj.get(orbital_days_col))
    if float(obj.get(orbital_days_col)) < orbital_days_min:
        orbital_days_min = float(obj.get(orbital_days_col))
    # Transit Epoch [BKJD]
    if float(obj.get(transit_epoch_col)) > transit_epoch_max:
        transit_epoch_max = float(obj.get(transit_epoch_col))
    if float(obj.get(transit_epoch_col)) < transit_epoch_min:
        transit_epoch_min = float(obj.get(transit_epoch_col))
    # Impact Parameter
    if float(obj.get(impact_parameter_col)) > impact_parameter_max:
        impact_parameter_max = float(obj.get(impact_parameter_col))
    if float(obj.get(impact_parameter_col)) < impact_parameter_min:
        impact_parameter_min = float(obj.get(impact_parameter_col))
    # Transit Duration [hrs]
    if float(obj.get(transit_duration_col)) > transit_duration_max:
        transit_duration_max = float(obj.get(transit_duration_col))
    if float(obj.get(transit_duration_col)) < transit_duration_min:
        transit_duration_min = float(obj.get(transit_duration_col))
    # Transit Depth [ppm]
    if float(obj.get(transit_depth_col)) > transit_depth_max:
        transit_depth_max = float(obj.get(transit_depth_col))
    if float(obj.get(transit_depth_col)) < transit_depth_min:
        transit_depth_min = float(obj.get(transit_depth_col))
    # Planetary Radius [Earth radii]
    if float(obj.get(planetary_radius_col)) > planetary_radius_max:
        planetary_radius_max = float(obj.get(planetary_radius_col))
    if float(obj.get(planetary_radius_col)) < planetary_radius_min:
        planetary_radius_min = float(obj.get(planetary_radius_col))
    # Equilibrium Temperature [K]
    if float(obj.get(equilibrium_temperature_col)) > equilibrium_temperature_max:
        equilibrium_temperature_max = float(obj.get(equilibrium_temperature_col))
    if float(obj.get(equilibrium_temperature_col)) < equilibrium_temperature_min:
        equilibrium_temperature_min = float(obj.get(equilibrium_temperature_col))
    # Insolation Flux [Earth flux]
    if float(obj.get(insolation_flux_col)) > insolation_flux_max:
        insolation_flux_max = float(obj.get(insolation_flux_col))
    if float(obj.get(insolation_flux_col)) < insolation_flux_min:
        insolation_flux_min = float(obj.get(insolation_flux_col))
    # Transit Signal-to-Noise
    if float(obj.get(transit_signal_to_noise_col)) > transit_signal_to_noise_max:
        transit_signal_to_noise_max = float(obj.get(transit_signal_to_noise_col))
    if float(obj.get(transit_signal_to_noise_col)) < transit_signal_to_noise_min:
        transit_signal_to_noise_min = float(obj.get(transit_signal_to_noise_col))
    # Stellar Effective Temperature [K]
    if float(obj.get(stellar_effective_temperature_col)) > stellar_effective_temperature_max:
        stellar_effective_temperature_max = float(obj.get(stellar_effective_temperature_col))
    if float(obj.get(stellar_effective_temperature_col)) < stellar_effective_temperature_min:
        stellar_effective_temperature_min = float(obj.get(stellar_effective_temperature_col))
    # Stellar Surface Gravity [log10(cm/s**2)]
    if float(obj.get(stellar_surface_gravity_col)) > stellar_surface_gravity_max:
        stellar_surface_gravity_max = float(obj.get(stellar_surface_gravity_col))
    if float(obj.get(stellar_surface_gravity_col)) < stellar_surface_gravity_min:
        stellar_surface_gravity_min = float(obj.get(stellar_surface_gravity_col))
    # Stellar Radius [Solar radii]
    if float(obj.get(stellar_radius_col)) > stellar_radius_max:
        stellar_radius_max = float(obj.get(stellar_radius_col))
    if float(obj.get(stellar_radius_col)) < stellar_radius_min:
        stellar_radius_min = float(obj.get(stellar_radius_col))
    # RA [decimal degrees]
    if float(obj.get(ra_col)) > ra_max:
        ra_max = float(obj.get(ra_col))
    if float(obj.get(ra_col)) < ra_min:
        ra_min = float(obj.get(ra_col))
    # Dec [decimal degrees]
    if float(obj.get(dec_col)) > dec_max:
        dec_max = float(obj.get(dec_col))
    if float(obj.get(dec_col)) < dec_min:
        dec_min = float(obj.get(dec_col))
    # Kepler-band [mag]
    if float(obj.get(kepler_band_col)) > kepler_band_max:
        kepler_band_max = float(obj.get(kepler_band_col))
    if float(obj.get(kepler_band_col)) < kepler_band_min:
        kepler_band_min = float(obj.get(kepler_band_col))

print(f"Orbital Period Max Value - {orbital_days_max} days")
print(f"Orbital Period Min Value - {orbital_days_min} days")  
print(f"Orbital Period Avg Value - {orbital_period_avg} days")

print(f"Transit Epoch Max Value - {transit_epoch_max} BKJD")
print(f"Transit Epoch Min Value - {transit_epoch_min} BKJD")
print(f"Transit Epoch Avg Value - {transit_epoch_avg} BKJD")

print(f"Impact Parameter Max Value - {impact_parameter_max}")
print(f"Impact Parameter Min Value - {impact_parameter_min}")
print(f"Impact Parameter Avg Value - {impact_parameter_avg}")

print(f"Transit Duration Max Value - {transit_duration_max} hours")
print(f"Transit Duration Min Value - {transit_duration_min} hours")
print(f"Transit Duration Avg Value - {transit_duration_avg} hours")

print(f"Transit Depth  Max Value - {transit_depth_max} ppm")
print(f"Transit Depth  Min Value - {transit_depth_min} ppm")
print(f"Transit Depth  Avg Value - {transit_depth_avg} ppm")

print(f"Planetary Radius  Max Value - {planetary_radius_max} Earth radii")
print(f"Planetary Radius  Min Value - {planetary_radius_min} Earth radii")
print(f"Planetary Radius  Avg Value - {planetary_radius_avg} Earth radii")

print(f"Equilibrium Temperature  Max Value - {equilibrium_temperature_max} K")
print(f"Equilibrium Temperature  Min Value - {equilibrium_temperature_min} K")
print(f"Equilibrium Temperature  Avg Value - {equilibrium_temperature_avg} K")

print(f"Insolation Flux Max Value - {insolation_flux_max} Earth flux")
print(f"Insolation Flux Min Value - {insolation_flux_min} Earth flux")
print(f"Insolation Flux Avg Value - {insolation_flux_avg} Earth flux")

print(f"Transit Signal-to-Noise Max Value - {transit_signal_to_noise_max}")
print(f"Transit Signal-to-Noise Min Value - {transit_signal_to_noise_min}")
print(f"Transit Signal-to-Noise Avg Value - {transit_signal_to_noise_avg}")

print(f"Stellar Effective Temperature Max Value - {stellar_effective_temperature_max} K")
print(f"Stellar Effective Temperature Min Value - {stellar_effective_temperature_min} K")
print(f"Stellar Effective Temperature Avg Value - {stellar_effective_temperature_avg} K")

print(f"Stellar Surface Gravity Max Value - {insolation_flux_max} log10(cm/s**2)")
print(f"Stellar Surface Gravity Min Value - {insolation_flux_min} log10(cm/s**2)")
print(f"Stellar Surface Gravity Avg Value - {insolation_flux_avg} log10(cm/s**2)")

print(f"Stellar Radius Max Value - {stellar_radius_max} Solar radii")
print(f"Stellar Radius Min Value - {stellar_radius_min} Solar radii")
print(f"Stellar Radius Avg Value - {stellar_radius_avg} Solar radii")

print(f"RA Max Value - {ra_max} decimal degrees")
print(f"RA Min Value - {ra_min} decimal degrees")
print(f"RA Avg Value - {ra_avg} decimal degrees")

print(f"Dec Max Value - {dec_max} decimal degrees")
print(f"Dec Min Value - {dec_min} decimal degrees")
print(f"Dec Avg Value - {dec_avg} decimal degrees")

print(f"Kepler-band Max Value - {kepler_band_max} mag")
print(f"Kepler-band Min Value - {kepler_band_min} mag")
print(f"Kepler-band Avg Value - {kepler_band_avg} mag")

# Standard Devation

orbital_period_standard_deviation = 0
orbital_period_values = []
for obj in detected_objects:
    for col in obj:
        if col == "Orbital Period [days]":
            orbital_period_values.append(float(obj.get(col)))

print(f"Orbital Period standard deviation - {statistics.stdev(orbital_period_values)}")

# Median of Variables

# Interquartile Ranges for Variables - IQR=Q3-Q1

# Quantile 0.1

# Quantile 0.9
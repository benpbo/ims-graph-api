# RECEIVE FROM USER:
# element = 'TEMP_MIN' / 'TEMP_MAX' / 'TEMP_AVG' / 'RAIN'
# data = {observations: bool, models: [list], senario: [list]}
# stations = ['AFULA', 'EILAT', ...] / ['ALL']
# data_time_range = ('1950', '2020') #make sure he puts good values
# line_time_range = ('1950', '2020')
# resolution = [1, 2] #this is the filter of months
# calculation = 'max' / 'min' / 'avg'
# show_all_models = True / False
# show_average = True / False
# show_line = True / False

# RECEIVE FROM DB QUERY:
# df_observations = Year, month, day, value, station
# df_predictions = year, month, day, value, station, model, scenario
# df_line = Year, month, day, value, station

import pandas as pd

### CONSTS ###

TEST_CSV = r'C:\Users\עינב\Documents\ecoton\test_table.csv'

# CSV DATA
TEST_CSV_AVG = r'C:\Users\עינב\Documents\ecoton\temperature_comb_stations_avg.csv'
TEST_CSV_MIN = r'C:\Users\עינב\Documents\ecoton\temperature_comb_stations_min.csv'
TEST_CSV_MAX = r'C:\Users\עינב\Documents\ecoton\temperature_comb_stations_max.csv'
TEST_CSV_MODEL_DOROT_MAX = r'C:\Users\עינב\Documents\ecoton\dorot_tmax_12models_rcp45_rcp85_qdm.csv'
TEST_CSV_MODEL_DOROT_MIN = r'C:\Users\עינב\Documents\ecoton\dorot_tmin_12models_rcp45_rcp85_qdm.csv'

# Colunms names
DATA_COL = 'value'
YEAR_COL = 'year'
MONTH_COL = 'month'
STATION_COL = 'station'
MODEL_COL = 'model'
SCENARIO_COL = 'scenario'

OBSERVATIONS_GRAPH_NAME = 'observation'
BASE_LINE = 'base line'

# optional functions
AVG_FUNC = pd.DataFrame.mean
MIN_FUNC = min
MAX_FUNC = max

# Get from user
data_time_range = ('1950', '2020')
line_time_range = ('1950', '2020')
show_all_models = True
show_average = True
show_line = True
calculation = MIN_FUNC
data = {'observations': True, 'models': ['cnrm_cclm', 'had_cclm', 'knmi_racm', 'mpi_remo', 'cccma_rca', 'cnrm_rca', 'csiro_rca', 'ipsl_rca', 'miroc_rca', 'had_rca', 'mpi_rca', 'noaa_rca'], 'scenario': ['rcp85']}

### FUNCTIONS ###

def get_relevant_stations(dfs) -> list:
    min_year = (10000, [])   # tuple of minimum year and the df that has the minimum year
    for df in dfs:
        if not df.empty:
            min_year = (min(min_year[0], df[YEAR_COL].min()), df)
    df = min_year[1]
    df = df[df[YEAR_COL] == min_year[0]]
    return list(df[STATION_COL].drop_duplicates())

def calculate_df(df, calculation_func) -> pd.DataFrame:
    if calculation_func in [MIN_FUNC, MAX_FUNC]:
        df = df.groupby([YEAR_COL, STATION_COL])[DATA_COL].apply(calculation_func)
        df = df.reset_index(level=0)
    return df.groupby(YEAR_COL)[DATA_COL].apply(pd.DataFrame.mean)

def df_add_col(original_df, new_col_name, data, calculation):
    return pd.concat([original_df, pd.DataFrame({new_col_name: calculate_df(data, calculation)})], axis=1, levels=0)

# QUERY DB
#********************** FILL
df_observations = pd.read_csv(TEST_CSV_MIN).dropna()
df_predictions = pd.read_csv(TEST_CSV_MODEL_DOROT_MIN).dropna()
df_line = pd.read_csv(TEST_CSV_MIN).dropna()

# calculate minimum year and return only relevant stations

stations_list = get_relevant_stations([df_observations, df_predictions, df_line])
fix_data = lambda df: df[df[STATION_COL].isin(stations_list)]
df_observations_new = fix_data(df_observations)
df_predictions_new = fix_data(df_predictions)

# calculate requested graphs and save them in a dataframe

df_graphs = pd.DataFrame()

if not df_observations_new.empty:
    df_graphs = df_add_col(df_graphs, OBSERVATIONS_GRAPH_NAME, df_observations_new, calculation)
if not df_predictions_new.empty:
    if show_all_models:
        model_list = df_predictions_new[MODEL_COL].drop_duplicates()
        for model in model_list:
            df_graphs = df_add_col(df_graphs, model, df_predictions_new[df_predictions_new[MODEL_COL] == model], calculation)
    if show_average:
        scenario_list = df_predictions_new[SCENARIO_COL].drop_duplicates()
        for scenario in scenario_list:
            df_graphs = df_add_col(df_graphs, scenario + '_avg', df_predictions_new[df_predictions_new[SCENARIO_COL] == scenario], calculation)
if not df_line.empty:
    if show_line:
        df_graphs[BASE_LINE] = calculate_df(df_line, calculation).mean()

# INSERT RETURN df_graph AS .json

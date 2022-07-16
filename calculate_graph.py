### IMPORTS ###

import pandas as pd

### CONSTS ###

TEST_CSV = r'C:\Users\עינב\Documents\ecoton\test_table.csv'

WINTER = [12, 1, 2]
SPRING = [3, 4, 5]
SUMMER = [6, 7, 8]
FALL = [9, 10, 11]

RES_YEAR = 'year'
RES_MONTH = 'month'
RES_SEASON = 'season'

DATA_COL = 'value'
YEAR_COL = 'Year'
MONTH_COL = 'Month'
STATION_COL = 'Station'

AVG_FUNC = pd.DataFrame.mean
MIN_FUNC = min
MAX_FUNC = max
THRESHHOLD_FUNC = 'thresh_hold'

### FUNCTIONS ###

def get_resolution(df, resolution=RES_YEAR, resolution_value=None):
    
    if resolution == RES_MONTH:
        return df[df[MONTH_COL] == resolution_value]
    if resolution == RES_SEASON:
        return df[df[MONTH_COL].isin(resolution_value)]

def calculate_df(df, calculation_func) -> pd.DataFrame:
    if calculation_func in [MIN_FUNC, MAX_FUNC]:
        df = df.groupby([YEAR_COL, STATION_COL])[DATA_COL].apply(calculation_func)
        df = df.reset_index(level=0)        
    return df.groupby(YEAR_COL)[DATA_COL].apply(AVG_FUNC)

def print_graph(df):
    df.plot()
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

from imp import release_lock
from typing import Iterable, Optional
import requests
import pandas as pd

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


def calculate_graphs(
        element: str,
        models_list: Iterable[str],
        scenarios: Iterable[str],
        stations_list: Iterable[str],
        resolution: Iterable[int],
        data_time_range: tuple[int, int],
        baseline_time_range: Optional[tuple[int, int]],
        show_all_models: bool,
        show_average: bool,
        calculation: str):

    match calculation:
        case 'Average':
            calculation = AVG_FUNC
        case 'Max':
            calculation = MAX_FUNC
        case 'Min':
            calculation = MIN_FUNC

    def get_relevant_stations(dfs) -> list:
        # tuple of minimum year and the df that has the minimum year
        min_year: tuple[int, list] = (10000, [])
        for df in dfs:
            if not df.empty:
                min_year = (min(min_year[0], df[YEAR_COL].min()), df)

        end_df = min_year[1]

        end_df = end_df[end_df[YEAR_COL] == min_year[0]]

        return list(end_df[STATION_COL].drop_duplicates())

    def calculate_df(df, calculation_func) -> pd.DataFrame:
        if calculation_func in [MIN_FUNC, MAX_FUNC]:
            df = df.groupby([YEAR_COL, STATION_COL])[
                DATA_COL].apply(calculation_func)
            df = df.reset_index(level=0)
        return df.groupby(YEAR_COL)[DATA_COL].apply(pd.DataFrame.mean)

    def df_add_col(original_df, new_col_name, data, calculation):
        return pd.concat([original_df, pd.DataFrame({new_col_name: calculate_df(data, calculation)})], axis=1, levels=0)

    # QUERY DB
    # ********************** FILL
    url = 'http://localhost:5000'
    start_year, end_year = data_time_range
    base_params = {
        'element': element,
        'station': stations_list,
        'start_year': start_year,
        'end_year': end_year,
        'month': [str(m) for m in resolution],
    }

    df_observations = pd.DataFrame()
    df_predictions = pd.DataFrame()
    df_line = pd.DataFrame()

    df_observations = pd.read_json(requests.get(
        f'{url}/graph/observations',
        params=base_params).text)
    if models_list:
        data_frames = [pd.read_json(requests.get(
            f'{url}/graph/predictions',
            params={
                **base_params,
                'model': models_list,
                'scenario': scenario,
            }).text)
            for scenario in scenarios]
        df_predictions = pd.concat(data_frames)
    if baseline_time_range:
        df_line = pd.read_json(requests.get(
            f'{url}/graph/observations',
            params={
                **base_params,
                'start_year': baseline_time_range[0],
                'end_year': baseline_time_range[1],
            }).text)

    # calculate minimum year and return only relevant stations
    stations_list = get_relevant_stations(
        [df_observations, df_predictions, df_line])

    def fix_data(df): return df[df[STATION_COL].isin(stations_list)]

    if not df_observations.empty:
        df_observations_new = fix_data(df_observations)
    else:
        df_observations_new = df_observations
    if not df_predictions.empty:
        df_predictions_new = fix_data(df_predictions)
    else:
        df_predictions_new = df_predictions

    # calculate requested graphs and save them in a dataframe
    df_graphs = pd.DataFrame()
    if not df_observations_new.empty:
        df_graphs = df_add_col(df_graphs, OBSERVATIONS_GRAPH_NAME,
                               df_observations_new, calculation)
    if not df_predictions_new.empty:
        if show_all_models:
            model_list = df_predictions_new[MODEL_COL].drop_duplicates()
            for model in model_list:
                df_graphs = df_add_col(
                    df_graphs, model, df_predictions_new[df_predictions_new[MODEL_COL] == model], calculation)
        if show_average:
            scenario_list = df_predictions_new[SCENARIO_COL].drop_duplicates()
            for scenario in scenario_list:
                df_graphs = df_add_col(
                    df_graphs, scenario + '_avg', df_predictions_new[df_predictions_new[SCENARIO_COL] == scenario], calculation)
    if not df_line.empty:
        if baseline_time_range:
            df_graphs[BASE_LINE] = calculate_df(df_line, calculation).mean()

    return df_graphs.to_json()

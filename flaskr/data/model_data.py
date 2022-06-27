from enum import Enum
from functools import reduce
from typing import Iterable

import pandas as pd
from pandas import DataFrame

from .common import REQUIRED_COLUMNS, VALUE_COL, Element

TEMP_MIN_COL = 'tmin'
TEMP_MAX_COL = 'tmax'
RAIN_MM_COL = 'pr'
SCENARIO_COL = 'scenario'
MODEL_COL = 'model'
STATION_COL = 'station'

RESOURCE_IDS = {
    (Element.TEMP_MIN, 'AFULA'): 'b0f78f49-923e-4492-aff5-39fc85750d48',
    (Element.TEMP_MAX, 'AFULA'): 'b0f78f49-923e-4492-aff5-39fc85750d48',
    (Element.TEMP_AVG, 'AFULA'): 'b0f78f49-923e-4492-aff5-39fc85750d48',
}


class Scenario(Enum):
    RCP45 = 'rcp45'
    RCP85 = 'rcp85'


def get_model_data(
        element: Element,
        station_names: Iterable[str],
        model_names: Iterable[str],
        scenario: Scenario) -> DataFrame:
    data = (
        _get_station_model_data(element, station_name, model_names, scenario)
        for station_name in station_names)

    return reduce(
        lambda sum, station_data: pd.concat((sum, station_data)),
        data)


def _get_station_model_data(
        element: Element,
        station_name: str,
        model_names: Iterable[str],
        scenario: Scenario) -> DataFrame:
    # Read csv
    resource_id = RESOURCE_IDS[(element, station_name)]
    file_name = f'{resource_id}.csv'
    df = pd.read_csv(file_name)

    # Filter for specific scenario and chosen models
    scenario_mask = df[SCENARIO_COL] == scenario.value
    model_mask = df[MODEL_COL].isin(model_names)
    df = df[scenario_mask & model_mask]

    # Add value column
    df = _add_value_column(df, element)

    # Return the dataframe with the required columns
    return df[REQUIRED_COLUMNS]


def _add_value_column(df: DataFrame, element: Element) -> DataFrame:
    match element:
        case Element.TEMP_MIN:
            return df.rename({TEMP_MIN_COL: VALUE_COL})
        case Element.TEMP_MAX:
            return df.rename({TEMP_MAX_COL: VALUE_COL})
        case Element.TEMP_AVG:
            df[VALUE_COL] = df[[TEMP_MIN_COL, TEMP_MAX_COL]].mean(axis=1)
            return df
        case Element.RAIN_MM:
            return df.rename({RAIN_MM_COL: VALUE_COL})

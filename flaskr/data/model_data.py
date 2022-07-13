from enum import Enum
from os import path
from typing import IO, Callable, Iterable

import pandas as pd
from pandas import DataFrame

from .common import STATION_COL, Element, transform_to_graph

SCENARIO_COL = 'scenario'
MODEL_COL = 'model'


class Scenario(Enum):
    RCP45 = 'rcp45'
    RCP85 = 'rcp85'


def get_model_data(
        reader: Callable[[str], IO],
        element: Element,
        station_names: Iterable[str],
        model_names: Iterable[str],
        scenario: Scenario) -> DataFrame:
    # Read csv
    file_name = path.join('db', 'models', f'{element.type}.csv')
    with reader(file_name) as file:
        df = pd.read_csv(file)

    # Apply filters
    station_mask = df[STATION_COL].isin(station_names)
    scenario_mask = df[SCENARIO_COL] == scenario.value
    model_mask = df[MODEL_COL].isin(model_names)
    df = df[station_mask & scenario_mask & model_mask]

    return transform_to_graph(df, element)

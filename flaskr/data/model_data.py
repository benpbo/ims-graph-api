from os import path
from typing import IO, Callable, Iterable

import pandas as pd
from pandas import DataFrame

from .common import Element
from .filters import ModelFilter, Scenario


def get_model_data(
        reader: Callable[[str], IO],
        element: Element,
        station_names: Iterable[str],
        model_names: Iterable[str],
        scenario: Scenario) -> DataFrame:
    # Read csv
    file_name = path.join('db', 'models', f'{element.type.name.lower()}.csv')
    with reader(file_name) as file:
        df = pd.read_csv(file)

    # Apply filters
    df_filter = ModelFilter(station_names, model_names, scenario)
    return df_filter.filter(df)

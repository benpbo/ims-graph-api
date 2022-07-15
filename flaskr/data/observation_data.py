from os import path
from typing import IO, Callable, Iterable

import pandas as pd
from pandas import DataFrame

from flaskr.data.filters import StationFilter

from .common import Element


def get_observation_data(
        reader: Callable[[str], IO],
        element: Element,
        station_names: Iterable[str]) -> DataFrame:
    # Read csv
    file_name = path.join('db', 'observations', f'{element.type}.csv')
    with reader(file_name) as file:
        df = pd.read_csv(file)

    # Apply filters
    df_filter = StationFilter(station_names)
    return df_filter.filter(df)

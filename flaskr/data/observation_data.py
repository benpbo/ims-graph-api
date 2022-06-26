from typing import Iterable

from pandas import DataFrame

from .common import Element


def get_observation_data(
        element: Element,
        station_names: Iterable[str]) -> DataFrame:
    raise NotImplementedError()

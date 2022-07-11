from typing import IO, Callable, Iterable

from pandas import DataFrame

from .common import Element


def get_observation_data(
        reader: Callable[[str], IO],
        element: Element,
        station_names: Iterable[str]) -> DataFrame:
    raise NotImplementedError()

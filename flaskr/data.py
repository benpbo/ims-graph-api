from enum import Enum, auto
from typing import Iterable

from pandas import DataFrame


class Scenario(Enum):
    RCP45 = 'rcp45'
    RCP85 = 'rcp85'


class Element(Enum):
    TEMP_MAX = auto()
    TEMP_MIN = auto()
    TEMP_AVG = auto()
    RAIN_MM = auto()


def get_observation_data(
        element: Element,
        station_names: Iterable[str]) -> DataFrame:
    raise NotImplementedError()


def get_model_data(
        element: Element,
        station_names: Iterable[str],
        model_names: Iterable[str],
        scenario: Scenario) -> DataFrame:
    raise NotImplementedError()

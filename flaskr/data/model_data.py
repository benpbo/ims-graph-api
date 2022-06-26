from enum import Enum
from typing import Iterable

from pandas import DataFrame

from .common import Element


class Scenario(Enum):
    RCP45 = 'rcp45'
    RCP85 = 'rcp85'


def get_model_data(
        element: Element,
        station_names: Iterable[str],
        model_names: Iterable[str],
        scenario: Scenario) -> DataFrame:
    raise NotImplementedError()

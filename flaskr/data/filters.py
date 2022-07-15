from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Iterable

from pandas import DataFrame, Series

from .common import RAIN_MM_COL, STATION_COL, TEMP_MAX_COL, TEMP_MIN_COL, YEAR_COL, ElementType

MISSING_OBSERVATION = -99.9
SCENARIO_COL = 'scenario'
MODEL_COL = 'model'


class Scenario(Enum):
    RCP45 = 'rcp45'
    RCP85 = 'rcp85'


class FilterBase(ABC):
    def filter(self, df: DataFrame) -> DataFrame:
        mask = self.create_mask(df)
        return df[mask]

    @abstractmethod
    def create_mask(self, df: DataFrame) -> Series[bool]:
        ...


class StationFilter(FilterBase):
    def __init__(self, stations: Iterable[str]) -> None:
        super().__init__()

        self._stations = stations

    def create_mask(self, df: DataFrame) -> Series[bool]:
        return df[STATION_COL].isin(self._stations)


class ObservationFilter(StationFilter):
    def __init__(self, stations: Iterable[str], element_type: ElementType) -> None:
        super().__init__(stations)

        self._element_type = element_type

    def create_mask(self, df: DataFrame) -> Series[bool]:
        match self._element_type:
            case ElementType.TEMPERATURE:
                mask = ~df[TEMP_MIN_COL].eq(MISSING_OBSERVATION) \
                    & ~df[TEMP_MAX_COL].eq(MISSING_OBSERVATION)
            case ElementType.RAIN:
                mask = ~df[RAIN_MM_COL].eq(MISSING_OBSERVATION)

        return super().create_mask(df) & mask


class ModelFilter(StationFilter):
    def __init__(
            self,
            stations: Iterable[str],
            models: Iterable[str],
            scenario: Scenario) -> None:
        super().__init__(stations)

        self._models = models
        self._scenario = scenario

    def create_mask(self, df: DataFrame) -> Series[bool]:
        return super().create_mask(df) \
            & df[MODEL_COL].isin(self._models) \
            & df[SCENARIO_COL].eq(self._scenario)

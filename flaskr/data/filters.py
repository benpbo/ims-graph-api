from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Iterable

from flask_sqlalchemy import BaseQuery, Model
from sqlalchemy import and_, or_

from .common import ElementType

MISSING_OBSERVATION = -99.9
SCENARIO_COL = 'scenario'
MODEL_COL = 'model'


class Scenario(Enum):
    RCP45 = 'rcp45'
    RCP85 = 'rcp85'


class FilterBase(ABC):
    def filter(self, table: Model, query: BaseQuery) -> BaseQuery:
        criterions = self.create_criterion(table)
        return query.filter(and_(*criterions))

    @abstractmethod
    def create_criterion(self, table: Model) -> Iterable:
        ...


class StationFilter(FilterBase):
    def __init__(self, stations: Iterable[str]) -> None:
        super().__init__()

        self._stations = stations

    def create_criterion(self, table: Model) -> Iterable:
        yield table.station.in_(self._stations)


class ObservationFilter(StationFilter):
    def __init__(self, stations: Iterable[str], element_type: ElementType) -> None:
        super().__init__(stations)

        self._element_type = element_type

    def create_criterion(self, table: Model) -> Iterable:
        yield from super().create_criterion(table)

        match self._element_type:
            case ElementType.TEMPERATURE:
                yield or_(
                    table.tmin == MISSING_OBSERVATION,
                    table.tmax == MISSING_OBSERVATION)
            case ElementType.RAIN:
                yield table.pr == MISSING_OBSERVATION


class PredictionFilter(StationFilter):
    def __init__(
            self,
            stations: Iterable[str],
            models: Iterable[str],
            scenario: Scenario) -> None:
        super().__init__(stations)

        self._models = models
        self._scenario = scenario

    def create_criterion(self, table: Model) -> Iterable:
        yield from super().create_criterion(table)
        yield table.model.in_(self._models)
        yield table.scenario == self._scenario

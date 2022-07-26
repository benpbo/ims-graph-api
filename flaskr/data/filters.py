from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Iterable

from flask_sqlalchemy import BaseQuery, Model
from sqlalchemy import Column, and_, or_

from .common import ElementType

MISSING_OBSERVATION = -99.9

class Scenario(str, Enum):
    RCP45 = 'rcp45'
    RCP85 = 'rcp85'


class FilterBase(ABC):
    def filter(self, table: Model, query: BaseQuery) -> BaseQuery:
        criterions = self.create_criterion(table)
        return query.filter(and_(*criterions))

    @abstractmethod
    def create_criterion(self, table: Model) -> Iterable:
        ...


class AggregateFilter(FilterBase):
    def __init__(self, *filters: FilterBase):
        super().__init__()

        self._filters = filters

    def create_criterion(self, table: Model) -> Iterable:
        for filter in self._filters:
            yield from filter.create_criterion(table)


class IsInFilter(FilterBase):
    def __init__(self, column: Column, values: Iterable) -> None:
        super().__init__()

        self._column = column
        self._values = values

    def create_criterion(self, table: Model) -> Iterable:
        yield self._column.in_(self._values)


class ObservationFilter(FilterBase):
    def __init__(self, element_type: ElementType) -> None:
        super().__init__()

        self._element_type = element_type

    def create_criterion(self, table: Model) -> Iterable:
        match self._element_type:
            case ElementType.TEMPERATURE:
                yield or_(
                    table.tmin == MISSING_OBSERVATION,
                    table.tmax == MISSING_OBSERVATION)
            case ElementType.RAIN:
                yield table.pr == MISSING_OBSERVATION


class PredictionFilter(FilterBase):
    def __init__(self, models: Iterable[str], scenario: Scenario) -> None:
        super().__init__()

        self._models = models
        self._scenario = scenario

    def create_criterion(self, table: Model) -> Iterable:
        yield table.model.in_(self._models)
        yield table.scenario == self._scenario

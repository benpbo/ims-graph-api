from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Iterable

from flask_sqlalchemy import BaseQuery, Model
from sqlalchemy import Column, and_


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


class EqualsFilter(FilterBase):
    def __init__(self, column: Column, value: Any) -> None:
        super().__init__()

        self._column = column
        self._value = value

    def create_criterion(self, table: Model) -> Iterable:
        yield self._column == self._value

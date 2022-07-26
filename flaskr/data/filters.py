from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Iterable

from flask_sqlalchemy import BaseQuery
from sqlalchemy import Column


class Scenario(str, Enum):
    RCP45 = 'rcp45'
    RCP85 = 'rcp85'


class FilterBase(ABC):
    def filter(self, query: BaseQuery) -> BaseQuery:
        criterions = self.create_criterion()
        return query.filter(*criterions)

    @abstractmethod
    def create_criterion(self) -> Iterable:
        ...


class AggregateFilter(FilterBase):
    def __init__(self, *filters: FilterBase):
        super().__init__()

        self._filters = filters

    def create_criterion(self) -> Iterable:
        for filter in self._filters:
            yield from filter.create_criterion()


class IsInFilter(FilterBase):
    def __init__(self, column: Column, values: Iterable) -> None:
        super().__init__()

        self._column = column
        self._values = values

    def create_criterion(self) -> Iterable:
        yield self._column.in_(self._values)


class EqualsFilter(FilterBase):
    def __init__(self, column: Column, value: Any) -> None:
        super().__init__()

        self._column = column
        self._value = value

    def create_criterion(self) -> Iterable:
        yield self._column == self._value


class LessThanEqualsFilter(FilterBase):
    def __init__(self, column: Column, value: Any) -> None:
        super().__init__()

        self._column = column
        self._value = value

    def create_criterion(self) -> Iterable:
        yield self._column <= self._value


class GreaterThanEqualsFilter(FilterBase):
    def __init__(self, column: Column, value: Any) -> None:
        super().__init__()

        self._column = column
        self._value = value

    def create_criterion(self) -> Iterable:
        yield self._column >= self._value

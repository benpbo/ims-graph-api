import pandas as pd
from flask_sqlalchemy import BaseQuery, Model

from .filters import FilterBase


def get_data(
        table: Model,
        query: BaseQuery,
        filter: FilterBase) -> pd.DataFrame:
    query = filter.filter(table, query)
    return pd.read_sql(query.statement, query.session.bind)
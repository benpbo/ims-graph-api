import pandas as pd
from flask_sqlalchemy import BaseQuery

from .filters import FilterBase


def get_data(
        query: BaseQuery,
        filter: FilterBase) -> pd.DataFrame:
    query = filter.filter(query)
    return pd.read_sql(query.statement, query.session.bind)

from enum import Enum, auto

from pandas import DataFrame

STATION_COL = 'station'
YEAR_COL = 'year'
MONTH_COL = 'month'
DAY_COL = 'day'
TEMP_MIN_COL = 'tmin'
TEMP_MAX_COL = 'tmax'
RAIN_MM_COL = 'pr'
SCENARIO_COL = 'scenario'
MODEL_COL = 'model'
VALUE_COL = 'value'
GRAPH_COLUMNS = [YEAR_COL, MONTH_COL, DAY_COL, VALUE_COL,
                 STATION_COL, SCENARIO_COL, MODEL_COL]


class Element(Enum):
    TEMP_MAX = auto()
    TEMP_MIN = auto()
    TEMP_AVG = auto()
    RAIN_MM = auto()


def transform_to_graph(df: DataFrame, element: Element) -> DataFrame:
    match element:
        case Element.TEMP_MIN:
            graph = df.rename(columns={TEMP_MIN_COL: VALUE_COL})
        case Element.TEMP_MAX:
            graph = df.rename(columns={TEMP_MAX_COL: VALUE_COL})
        case Element.TEMP_AVG:
            temp_avg = df[[TEMP_MIN_COL, TEMP_MAX_COL]].mean(axis=1)
            graph = df.assign(**{VALUE_COL: temp_avg})
        case Element.RAIN_MM:
            graph = df.rename(columns={RAIN_MM_COL: VALUE_COL})

    return graph[graph.columns.intersection(GRAPH_COLUMNS)]

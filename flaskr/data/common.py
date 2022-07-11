from enum import Enum, auto


class Element(Enum):
    TEMP_MAX = auto()
    TEMP_MIN = auto()
    TEMP_AVG = auto()
    RAIN_MM = auto()

    @property
    def type(self) -> str:
        match self:
            case Element.TEMP_MIN | Element.TEMP_MAX | Element.TEMP_AVG:
                return 'temperature'
            case Element.RAIN_MM:
                return 'rain'


YEAR_COL = 'year'
MONTH_COL = 'month'
DAY_COL = 'day'
VALUE_COL = 'value'
REQUIRED_COLUMNS = [YEAR_COL, MONTH_COL, DAY_COL, VALUE_COL]

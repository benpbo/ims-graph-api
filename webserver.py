from typing import Iterable, Optional, Union
import streamlit as st
import pandas as pd
from calculate_graphs import calculate_graphs

### CONSTS ###
ELEMENTS = ['TEMP_MIN', 'TEMP_MAX', 'TEMP_AVG', 'RAIN']
MODELS = ['cnrm_cclm', 'had_cclm', 'knmi_racm', 'mpi_remo', 'cccma_rca', 'cnrm_rca',
          'csiro_rca', 'ipsl_rca', 'miroc_rca', 'had_rca', 'mpi_rca', 'noaa_rca']
SCENARIOS = ['RCP45', 'RCP85']
TEMPERATURE_STATIONS = ['afula', 'akko', 'avne_etan', 'beer_sheva', 'beit_jimal', 'besor_farm', 'bet_dagan', 'bet_zayda', 'dafna', 'dorot', 'elat', 'eLON', 'en_hahoresh', 'galed', 'gat', 'harashim', 'hazerim', 'hazeva', 'jerusalem_centre',
                        'kefar_blum', 'kefar_yehoshua', 'lahav', 'merom_golan', 'negba', 'qevuzat_yavne', 'rosh_zurim', 'sede_boqer', 'sede_eliyyahu', 'sedom', 'tavor_kadoorie', 'tel_aviv_coast', 'yotvata', 'zefat_har_kenaan', 'zemah']
RAIN_STATIONS = []  # ***FILL!!!
MONTHS = list(range(1, 12 + 1))
CALCULATIONS = ['Average', 'Max', 'Min']

OBSERVATIONS_TIME_RANGE = (1950, 2017)
PROJECTIONS_TIME_RANGE = (2006, 2100)
MIXED_TIME_RANGE = (
    min(OBSERVATIONS_TIME_RANGE[0], PROJECTIONS_TIME_RANGE[0]),
    max(OBSERVATIONS_TIME_RANGE[1], PROJECTIONS_TIME_RANGE[1]),
)

MODEL_COL = 'model'
SCENARIO_COL = 'scenario'

TEXT_CHOOSE = 'Choose the {0} you want to use'

CSV_DOWNLOAD_NAME = 'df.csv'


class UserInput:
    def __init__(self,
                 element: str,
                 models_list: Iterable[str],
                 scenarios_list: Iterable[str],
                 station_list: Iterable[str],
                 resolution: Iterable[int],
                 data_time_range: tuple[int, int],
                 baseline_time_range: Optional[tuple[int, int]],
                 show_all_models: bool,
                 show_average: bool,
                 calculation: str) -> None:
        self.element = element
        self.models_list = models_list
        self.scenarios_list = scenarios_list
        self.station_list = station_list
        self.resolution = resolution
        self.data_time_range = data_time_range
        self.baseline_time_range = baseline_time_range
        self.show_all_models = show_all_models
        self.show_average = show_average
        self.calculation = calculation


def create_checkbox_group(group_data):
    checkboxes = [st.checkbox(str(item)) for item in group_data]
    return [box for box in checkboxes if box]


def get_input() -> Union[UserInput, str]:
    element = st.radio(TEXT_CHOOSE.format('element'), ELEMENTS)

    available_stations: list[str]
    match element:
        case 'RAIN':
            available_stations = RAIN_STATIONS
        case 'TEMP_MIN' | 'TEMP_MAX' | 'TEMP_AVG':
            available_stations = TEMPERATURE_STATIONS
        case _:
            return f'No stations for element: "{element}"'

    st.write(TEXT_CHOOSE.format('data source'))
    observations = st.checkbox('Observations')
    projections = st.checkbox('Projections')

    data_range: tuple[int, int]
    match (observations, projections):
        case (True, False):
            data_range = OBSERVATIONS_TIME_RANGE
        case (False, True):
            data_range = PROJECTIONS_TIME_RANGE
        case (True, True):
            data_range = (
                min(OBSERVATIONS_TIME_RANGE[0], PROJECTIONS_TIME_RANGE[0]),
                max(OBSERVATIONS_TIME_RANGE[1], PROJECTIONS_TIME_RANGE[1]),
            )
        case _:
            return 'Please select either observations or projections'

    time_range_min, time_range_max = data_range
    data_range_values: list[int] = list(range(
        time_range_min,
        time_range_max + 1))

    models_list: Optional[list[str]] = None
    scenarios_list: Optional[list[str]] = None
    if projections:
        models_list = st.multiselect(
            TEXT_CHOOSE.format('models'), MODELS)
        scenarios_list = st.multiselect(
            TEXT_CHOOSE.format('scenarios'), SCENARIOS)

    station_list = st.multiselect(
        TEXT_CHOOSE.format('stations'), available_stations)
    if not station_list:
        return 'Please select a station'

    selected_data_range = st.select_slider(
        'Select the period range (years)',
        options=data_range_values,
        value=data_range)

    resolution = st.multiselect(TEXT_CHOOSE.format('months'), MONTHS)
    calculation = st.radio(
        TEXT_CHOOSE.format('calculations'), CALCULATIONS)

    show_all_models: bool = False
    show_average: bool = False
    if projections:
        st.write('Choose graph settings:')
        show_all_models = st.checkbox('Show all models')
        show_average = st.checkbox('Show ensemble-mean models')

    st.write('Base line:')
    selected_baseline_range: Optional[tuple[int, int]] = None
    if st.checkbox('Add base line'):
        baseline_range_min, baseline_range_max = OBSERVATIONS_TIME_RANGE
        baseline_range_values: list[int] = list(range(
            baseline_range_min,
            baseline_range_max + 1))

        selected_baseline_range = st.select_slider(
            'Select the reference period (years)',
            options=baseline_range_values,
            value=OBSERVATIONS_TIME_RANGE)

    return UserInput(element,
                     models_list,
                     scenarios_list,
                     station_list,
                     resolution,
                     selected_data_range,
                     selected_baseline_range,
                     show_all_models,
                     show_average,
                     calculation)


def print_graph(input: UserInput):
    df = calculate_graphs(input.element,
                          input.models_list,
                          input.scenarios_list,
                          input.station_list,
                          input.resolution,
                          input.data_time_range,
                          input.baseline_time_range,
                          input.show_all_models,
                          input.show_average,
                          input.calculation)
    graph_df = pd.read_json(df)

    st.write('Graph:')
    st.line_chart(graph_df)

    st.download_button(
        label='Download data as CSV',
        data=graph_df.to_csv().encode('utf-8'),
        file_name=CSV_DOWNLOAD_NAME,
        mime='text/csv',
    )


def main():
    match get_input():
        case UserInput() as input:
            if st.button('Print Graph'):
                print_graph(input)
        case str() as error_message:
            st.error(error_message)


if __name__ == '__main__':
    main()

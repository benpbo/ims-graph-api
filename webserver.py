import streamlit as st
import pandas as pd

### CONSTS ###
ELEMENTS = ['TEMP_MIN', 'TEMP_MAX', 'TEMP_AVG', 'RAIN']
MODELS = ['cnrm_cclm','had_cclm','knmi_racm','mpi_remo','cccma_rca','cnrm_rca','csiro_rca','ipsl_rca','miroc_rca','had_rca','mpi_rca','noaa_rca']
SCENARIOS = ['rcp45', 'rcp85']
STATIONS_TEMP = ['AFULA', 'AKKO', 'AVNE_ETAN', 'BEER_SHEVA', 'BEIT_JIMAL', 'BESOR_FARM', 'BET_DAGAN', 'BET_ZAYDA', 'DAFNA', 'DOROT', 'ELAT', 'Elon', 'EN_HAHORESH', 'GALED', 'GAT', 'HARASHIM', 'HAZERIM', 'HAZEVA', 'JERUSALEM_CENTRE', 'KEFAR_BLUM', 'KEFAR_YEHOSHUA', 'LAHAV', 'MEROM_GOLAN', 'NEGBA', 'QEVUZAT_YAVNE', 'ROSH_ZURIM', 'SEDE_BOQER', 'SEDE_ELIYYAHU', 'SEDOM', 'TAVOR_KADOORIE', 'TEL_AVIV_COAST', 'YOTVATA', 'ZEFAT_HAR_KENAAN', 'ZEMAH']
STATIONS_RAIN = [] ## ***FILL!!!
MONTHS = list(range(1, 12 + 1))
CALCULATIONS = ['Average', 'Max', 'Min']

MIN_OBSV_YEAR = 1950
MAX_OBSV_YEAR = 2017
MIN_PRED_YEAR = 2006
MAX_PRED_YEAR = 2100

MODEL_COL = 'model'
SCENARIO_COL = 'scenario'

TEXT_CHOOSE = 'Choose the {0} you want to use'

### GLOBALS ###

element = None
observations = None
predictions = None
models_list = None
scenarios_list = None
station_list = None
data_time_range = None
line_time_range = None
resolution = None
calculation = None
show_all_models = None
show_average = None
show_line = None

### FUNCTIONS ###

def create_checkbox_group(group_data):
	checkboxes = [st.checkbox(str(item)) for item in group_data]
	return [box for box in checkboxes if box]

def user_inputs():

	element = st.radio(TEXT_CHOOSE.format('element'), ELEMENTS)

	st.write(TEXT_CHOOSE.format('data'))
	observations = st.checkbox('Observations')
	predictions = st.checkbox('Predictions')
	if predictions:
		st.write(TEXT_CHOOSE.format('models'))
		models_list = create_checkbox_group(MODELS)
		st.write(TEXT_CHOOSE.format('scenarios'))
		scenarios_list = create_checkbox_group(SCENARIOS)

	st.write(TEXT_CHOOSE.format('stations'))
	if element == 'RAIN':
		station_list = create_checkbox_group(STATIONS_RAIN)
	else:
		station_list = create_checkbox_group(STATIONS_TEMP)

	time_range_min = MIN_PRED_YEAR
	time_range_max = MAX_OBSV_YEAR
	if observations:
		time_range_min = MIN_OBSV_YEAR
	if predictions:
		time_range_max = MAX_PRED_YEAR
	data_time_range = st.select_slider('Select the time range of years for graph', options=list(range(time_range_min, time_range_max + 1)), value=(time_range_min, time_range_max))
	line_time_range = st.select_slider('Select the time range of years for base line', options=list(range(time_range_min, time_range_max + 1)), value=(time_range_min, time_range_max))

	st.write(TEXT_CHOOSE.format('months'))
	resolution = create_checkbox_group(MONTHS)

	calculation = st.radio(TEXT_CHOOSE.format('calculations'), CALCULATIONS)

	st.write('Choose graph settings:')
	show_all_models = st.checkbox('show all models')
	show_average = st.checkbox('show average')
	show_line = st.checkbox('show base line')



### MAIN ###
user_inputs()

EXAMPLE_DF = pd.DataFrame([[1, 2],[3, 4]])

st.line_chart(EXAMPLE_DF)
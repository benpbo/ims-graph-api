import streamlit as st
import pandas as pd

### CONSTS ###
ELEMENTS = ['TEMP_MIN', 'TEMP_MAX', 'TEMP_AVG', 'RAIN']
MODELS = ['cnrm_cclm','had_cclm','knmi_racm','mpi_remo','cccma_rca','cnrm_rca','csiro_rca','ipsl_rca','miroc_rca','had_rca','mpi_rca','noaa_rca']
SCENARIOS = ['RCP45', 'RCP85']
STATIONS_TEMP = ['afula', 'akko', 'avne_etan', 'beer_sheva', 'beit_jimal', 'besor_farm', 'bet_dagan', 'bet_zayda', 'dafna', 'dorot', 'elat', 'eLON', 'en_hahoresh', 'galed', 'gat', 'harashim', 'hazerim', 'hazeva', 'jerusalem_centre', 'kefar_blum', 'kefar_yehoshua', 'lahav', 'merom_golan', 'negba', 'qevuzat_yavne', 'rosh_zurim', 'sede_boqer', 'sede_eliyyahu', 'sedom', 'tavor_kadoorie', 'tel_aviv_coast', 'yotvata', 'zefat_har_kenaan', 'zemah']
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

CSV_DOWNLOAD_NAME = 'df.csv'

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
	predictions = st.checkbox('Projections')
	if predictions:
		st.write(TEXT_CHOOSE.format('models'))
		models_list = create_checkbox_group(MODELS)
		st.write(TEXT_CHOOSE.format('scenarios'))
		scenarios_list = create_checkbox_group(SCENARIOS)

	#st.write(TEXT_CHOOSE.format('stations'))
	if element == 'RAIN':
		station_list = st.multiselect(TEXT_CHOOSE.format('stations'), STATIONS_RAIN)
	else:
		station_list = st.multiselect(TEXT_CHOOSE.format('stations'), STATIONS_TEMP)

	if observations or predictions:
		time_range_min = MIN_PRED_YEAR
		time_range_max = MAX_OBSV_YEAR
		if observations:
			time_range_min = MIN_OBSV_YEAR
		if predictions:
			time_range_max = MAX_PRED_YEAR
		data_time_range = st.select_slider('Select the period range (years)', options=list(
			range(time_range_min, time_range_max + 1)), value=(time_range_min, time_range_max))

	st.write(TEXT_CHOOSE.format('months'))
	resolution = create_checkbox_group(MONTHS)

	calculation = st.radio(TEXT_CHOOSE.format('calculations'), CALCULATIONS)

	st.write('Choose graph settings:')
	show_all_models = st.checkbox('Show all models')
	show_average = st.checkbox('Show ensemble-mean models')

	st.write('Add base line')
	show_line = st.checkbox('Add base line')
	if show_line:
		line_time_range = st.select_slider('Select the reference period (years)', options=list(
			range(time_range_min, time_range_max + 1)), value=(time_range_min, time_range_max))


### MAIN ###
user_inputs()
#query_db()
#get_df
EXAMPLE_DF = pd.DataFrame([[1, 2],[3, 4]])
graph_df = EXAMPLE_DF
#print df
st.write('Graph:')
st.line_chart(graph_df)

st.download_button(
    label="Download data as CSV",
    data=graph_df.to_csv().encode('utf-8'),
    file_name=CSV_DOWNLOAD_NAME,
    mime='text/csv',
)

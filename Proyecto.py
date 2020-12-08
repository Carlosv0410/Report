# Proyecto

# Librerias a importar Streamlit, Pandas y Altair
import streamlit as st
import pandas as pd 
import altair as alt

# Librerias para importar imagenes y lectura de archivos Excel
from PIL import Image
from pandas import read_excel

#Cargar bases
image1 = Image.open('Geopolitical_map_of_Canada.JPG')

# Inicio de la aplicación
st.sidebar.title('Report')
selectbox_side_bar=st.sidebar.selectbox(
    "Select",
    ("Wellcome","1. Demographics","2. Knowledge"), index=0)

# Primera selección "Bienvenida"  en la caja de opciones 
if 	selectbox_side_bar == "Wellcome":
	st.title("Report on Telephone Survey Data from Ontario and Saskatchewan")
	
	st.image(image1, caption='Geopolitical map of Canada',
	          use_column_width=True)
if 	selectbox_side_bar == "1. Demographics":
	st.title("Demographics")
	selectbox1=st.selectbox(
    "Select",
    ("1.1. Location","1.2. Gender", "1.6. Age"), index=0)

	if 	selectbox1 == "1.1. Location":
		st.write("""
		|Location|Frequency|Percent|Cumulative|
		|-|-|-|-|
		|Ontario|1,008|49.85|49.85|
		|Saskatchewan|1,014|50.15|100.00|
		|**Total**|**2.022**|**100.00**|
		 """)
		ciudad = ["Saskatchewan", "Ontario"]
		latitud = [50.4547, 49.417] 
		longitud = [-104.607 ,  -82.433]

		data_map = {"lat": latitud,
					"lon": longitud}

		df_location = pd.DataFrame(data_map)
	
		st.map(df_location)

	if 	selectbox1 == "1.2. Gender":
		st.write("""
		|Gender|Onatrio|Saskatchewan|Grand Total|
		|-|-|-|-|
		|Refused|2|2|**4**|
		|Female|500|517|**1,017**|
		|Male|503|492|**995**|
		|Other|3|3|**6**|
		|**Grand Total**|**1,008**|**1,014**|**2,022**|
		 """)


		Gender = ["Refused","Female", "Male", "Other"]
		Ontario = [2,500,503,3]
		Saskatchewan =[2,517,492,3]

		data_gender = {"Gender": Gender,
					   "Ontario": Ontario,
					   "Saskatchewan":Saskatchewan}		
		
		df_gender = pd.DataFrame(data_gender)
		df2_gender= pd.melt(df_gender, id_vars=['Gender'], var_name='City' , value_name='Sample')

		df2_graf = alt.Chart(df2_gender).mark_bar().encode(
	    x='City',
	    y='Sample',
	    color = 'City',
	    column = 'Gender',
	    tooltip=['Sample']
	    ).interactive().properties( title = 'Demographics')

		st.altair_chart(df2_graf)

	if 	selectbox1 == "1.6. Age":
		year_of_bird = ["1925-1929","1030-1934","1935-1939","1940-1944","1945-1949","1950-1954","1955-1959","1960-1964","1965-1969","1970-1974","1975-1979","1980-1984","1985-1989","1990-1994","1995-1999","2000-2001","Refused"]
		ontario_age = [9,23,47,91,115,123,120,116,76,65,62,34,21,25,20,7,54]
		saskatchewan_age = [12,35,44,85,143,156,137,111,62,57,39,37,15,18,13,8,42]
		total_age = [21,58,91,176,258,279,257,227,138,122,101,71,36,43,33,15,96]
		percent_age = [1.04,2.87,4.50,8.70,12.76,13.80,12.71,11.23,6.82,6.03,5.00,3.51,1.78,2.13,1.63,0.74,4.75]

		data_age = {"Year of birth":year_of_bird,
					"Ontario":ontario_age,
					"Saskatchewan":saskatchewan_age}
		df_age = pd.DataFrame(data_age)
		st.write(df_age)
		df2_age= pd.melt(df_age, id_vars=['Year of birth'], var_name='City' , value_name='Sample')

		brush = alt.selection(type='interval')

		points = alt.Chart(df2_age).mark_point().encode(
		    x='Year of birth',
		    y='Sample',
		    color=alt.condition(brush, 'City', alt.value('lightgray'))
		).add_selection(
		    brush
		)

		bars = alt.Chart(df2_age).mark_bar().encode(
		    y='City',
		    color='City',
		    x='Sample'
		).transform_filter(
		    brush
		)

		grafico_capas = points & bars
		st.altair_chart(grafico_capas)
if  selectbox_side_bar == "2. Knowledge":

	st.title("Knowledge")

	knowledge = ["Do not know","Good","Moderate","Poor","Very good","Very poor"]
	knowledge_on = [8,205,419,202,112,62]
	knowledge_sk = [5,230,415,204,88,72]
	data_knowledge = {"Knowledge": knowledge,
					  "ON": knowledge_on,
					  "SK":knowledge_sk}
	df_knowledge = pd.DataFrame(data_knowledge)
	df2_knowledge= pd.melt(df_knowledge, id_vars=['Knowledge'], var_name='City' , value_name='Sample')

	st.write(df_knowledge)

	histograma_margen =	alt.Chart(df2_knowledge).mark_bar(color='red').encode(
   		alt.X("Sample", bin=True),
		y='count()',
   		).interactive().properties(  width=250, height=200)

	media = alt.Chart(df2_knowledge).mark_rule(color='black').encode(
	    x='mean(Sample)',
	    size=alt.value(5),
	)
		

	orden_margen = alt.Chart(df2_knowledge).mark_bar(color='gold').encode(
	    x='Sample',
	    y=alt.Y('Sample', sort='-x')
	).interactive().properties(  width=250, height=200)


	st.altair_chart(histograma_margen+media|orden_margen)


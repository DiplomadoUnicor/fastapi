from random import random
from turtle import color
import streamlit as st
import requests
import pandas as pd
import plotly.express as px 
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns

# swifter para apply lambda

st.set_page_config(layout = "wide")

@st.cache
def cargar_datos():
    return pd.read_csv('book.csv', dtype={'CODIGO DANE': str})
#st.header("Violencia Intrafamiliar en Colombia")
st.sidebar.header("Violencia intrafamiliar")
st.sidebar.markdown("---")

df=cargar_datos()
st.dataframe(df)

st.header("Casos de violencia intrafamiliar en Colombia de acuerdo al Departamento")
st.markdown("---")


st.sidebar.markdown("### **Seleccionar Departamento:**")
sorted_departamento = df.groupby('DEPARTAMENTO')['CANTIDAD'].count().sort_values(ascending=True).copy().index


select_departamento = []
select_departamento.append(st.sidebar.selectbox('', sorted_departamento))


#Filter df based on selection
departamento_df = df[df['DEPARTAMENTO'].isin(select_departamento)].copy()



col1, col2, col3 = st.columns(3)
    

with col1:
    st.markdown(f"*Cantidad de casos :* {departamento_df.shape[0]}")
    st.markdown(f"*Tipo de arma usada:* {np.max(departamento_df['ARMAS MEDIOS'])}")
   
with col2:
    st.markdown(f"*Rango mas alto correspondiente al municipio de:*  {np.max(departamento_df['MUNICIPIO'])}")
    st.markdown(f"*Rango mas bajo correspondiente al municipio de:*  {np.min(departamento_df['MUNICIPIO'])}")

with col3:
    st.markdown(f"*Genero mas Afectado:*  {np.min(departamento_df['GENERO'])}")
    



datos_agrupados = df[['MUNICIPIO', 'ARMAS MEDIOS','GENERO', 'GRUPO ETARIO', 'CANTIDAD']].copy()

newdf= df[['MUNICIPIO', 'ARMAS MEDIOS','GENERO', 'GRUPO ETARIO', 'CANTIDAD']].copy()
new_df_agrupado = newdf.copy()

#####################  SLIDER   ###################################33
lista_municipio = list(departamento_df['MUNICIPIO'].unique())

st.sidebar.markdown("*Lista de casos de acuerdo al municipio*")

opcion_municipio = st.sidebar.selectbox(label= "selecciona un municipio", options= lista_municipio)

st.markdown("---")
#st.dataframe(datos_agrupados[datos_agrupados['MUNICIPIO']==opcion_departamento])
otras_variables = list(datos_agrupados.columns)
otras_variables.pop(otras_variables.index('CANTIDAD'))
otras_variables.pop(otras_variables.index('MUNICIPIO'))
#otras_variable.pop(otras_variables.index('GRUPO ETARIO'))

opcion_y=st.sidebar.selectbox(label="selecciona una variable a evaluar",options=otras_variables)


st.sidebar.markdown("*Lista de casos de acuerdo al municipio*")


#Grafica de Barras
@st.cache
def plot_simple(df: pd.DataFrame, x: pd.DataFrame, y, sales_filter: str):
    data = df.copy()
    
    data = data[data["GRUPO ETARIO"] == sales_filter]
    fig = px.histogram(data, x=x, y=y, color=opcion_y, title=opcion_y)
    return fig, data 
plot, d = plot_simple(datos_agrupados,opcion_y,  "CANTIDAD",  opcion_municipio)


otras = list(df['GRUPO ETARIO'].unique())


opcion_grupo = st.sidebar.selectbox(label= "selecciona un GRUPO", options= otras)

@st.cache
def pie_simple(df: pd.DataFrame, x: pd.DataFrame, y, grupo_filter: str):
    data = df.copy()
    data = data[data["GENERO"] == grupo_filter]
    fig = px.bar(df, x=x, y=y, color=['green', 'blue', 'yellow'], title=opcion_y)
    return fig, data

pl, c = pie_simple(datos_agrupados,opcion_y,  "CANTIDAD",  opcion_grupo)
#st.plotly_chart(pl,use_container_width=True)
#color_discrete_sequence


col1, col2 = st.columns(2)



with col1: 
    st.plotly_chart(plot)

with col2:
    st.dataframe(c)



st.plotly_chart(pl, use_container_width=True)

# fecha=df.copy()
# fecha_asdate = fecha

# fecha_asdate['FECHA HECHO']= pd.to_datetime(fecha_asdate['FECHA HECHO'])

# fecha_asdate['AÑO']= fecha_asdate['FECHA HECHO'].apply(lambda x: x.year)
# fecha_asdate['MES']= fecha_asdate['FECHA HECHO'].apply(lambda x: x.month)
# fecha_asdate['DIA']= fecha_asdate['FECHA HECHO'].apply(lambda x: x.day)




# colors=[ "yellow", "orange", "blue", "red", "green"]
# pie=df['GRUPO ETARIO'].value_counts().plot(kind='pie',colors=colors, shadow=True, autopct = '% 1.1f%%',startangle=30, radius=1.1,center=(0.5,0.5),
#             textprops={'fontsize':12}, frame=False,pctdistance=.65)

# st.plotly_chart(plt.show(), use_container_width=True)


###################################################################################3
# genero=df.copy()

# #lista_año = list(fecha_asdate['AÑO'].unique())
# #otras_variables.pop(otras_variables('MUNICIPIO'))
# #st.dataframe(otras_variables)

# pie_data = fecha_asdate.groupby('AÑO')['GENERO'].count()

# # @st.cache
# # def grafico_pie(df: pd.DataFrame, x: pd.DataFrame, y, Nom_municipio_filter: str):
# #     data = df.copy()
# #     data = data[data["GRUPO ETARIO"] == Nom_municipio_filter]
# #     fig = px.pie(data, values=x, names=y)
# #     return fig, data


# # plot, d = plot_simple(datos_agrupados,opcion_y,  "CANTIDAD",  opcion_municipio)
# # st.plotly_chart(plot,use_container_width=True)
# # st.plotly_chart(plot)
# lista_grupo = list(df['GRUPO ETARIO'].unique())

# #st.sidebar.markdown("*Lista de casos de acuerdo al municipio*")

# opcion_grupo = st.sidebar.selectbox(label= "selecciona un GRUPO", options= lista_grupo)













# def plot_graphy2(fecha_asdate: pd.DataFrame, x: pd.DataFrame, y, sales_filter: str):
#     datos = fecha_asdate.copy()
#     datos= datos[datos["GENERO"] == sales_filter]
#     fig = px.bar(datos, x=x, y=y)
#     return fig, datos
# plot, f = plot_graphy2(fecha_asdate['ARMAS MEDIOS'], fecha_asdate['AÑO'], 'CANTIDAD', opcion_municipio)


# st.plotly_chart(plot)




# fig, ax = plt.subplots(figsize=(15,5))
# sns.lineplot(x='FECHA HECHO', y='CANTIDAD',data=df.loc['2010':'2020'])
#############################################################################3







# genero=df.copy()
# fecha=df.copy()
# fecha_asdate = fecha

# fecha_asdate['FECHA HECHO']= pd.to_datetime(fecha_asdate['FECHA HECHO'])

# fecha_asdate['AÑO']= fecha_asdate['FECHA HECHO'].apply(lambda x: x.year)
# fecha_asdate['MES']= fecha_asdate['FECHA HECHO'].apply(lambda x: x.month)
# fecha_asdate['DIA']= fecha_asdate['FECHA HECHO'].apply(lambda x: x.day)

# lista_año = list(fecha_asdate['AÑO'].unique())


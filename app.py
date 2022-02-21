from pyparsing import col
import streamlit as st
import requests
import pandas as pd
import plotly.express as px 
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# swifter para apply lambda

st.set_page_config(layout = "wide")
st.title('Violencia intrafamiliar en colombia')

@st.cache
def cargar_datos():
    return pd.read_csv('book.csv', dtype={'CODIGO DANE': str})
#st.header("Violencia Intrafamiliar en Colombia")
st.sidebar.header("Violencia intrafamiliar")
st.sidebar.markdown("---")

df=cargar_datos()
st.dataframe(df)

melted_asdate = df.copy()

melted_asdate['FECHA HECHO']= pd.to_datetime(melted_asdate['FECHA HECHO'])
melted_asdate['AÑO']= melted_asdate['FECHA HECHO'].apply(lambda x: x.year)
melted_asdate['MES']= melted_asdate['FECHA HECHO'].apply(lambda x: x.month)
melted_asdate['DIA']= melted_asdate['FECHA HECHO'].apply(lambda x: x.day)


st.header("Casos de violencia intrafamiliar en Colombia de acuerdo al Departamento")
st.markdown("---")


st.sidebar.markdown("### **Seleccionar Departamento:**")
##########################################3
#sor_año = melted_asdate.groupby('AÑO')['CANTIDAD'].count().sort_values(ascending=True).copy().index
#select_año = []
#select_año.append(st.sidebar.selectbox('', sor_año))

sorted_departamento = melted_asdate.groupby('DEPARTAMENTO')['CANTIDAD'].count().sort_values(ascending=True).copy().index
select_departamento = []
select_departamento.append(st.sidebar.selectbox('', sorted_departamento))
#######################################3
#año_df = melted_asdate[melted_asdate['AÑO'].isin(select_año)].copy()

departamento_df = melted_asdate[melted_asdate['DEPARTAMENTO'].isin(select_departamento)].copy()
#####################################################3
#datos_agrupados = df[['MUNICIPIO', 'ARMAS MEDIOS','GENERO', 'GRUPO ETARIO', 'CANTIDAD']].copy()
datoagrupado = melted_asdate[['MUNICIPIO', 'ARMAS MEDIOS','GENERO', 'GRUPO ETARIO','CANTIDAD','AÑO', 'MES', 'DIA']].copy()

###########################################
lista_departamentos = list(departamento_df['MUNICIPIO'].unique())
st.sidebar.markdown("*Lista de casos de acuerdo al municipio*")
opcion_departamento = st.sidebar.selectbox(label= "selecciona un municipio", options= lista_departamentos)

# lista_mes = list(año_df['MES'].unique())
# st.sidebar.markdown("*Lista de casos de acuerdo al MES*")
#opcion_mes = st.sidebar.selectbox(label= "selecciona un mes", options= lista_mes)
######################################3


st.sidebar.markdown("---")

otras_variables = list(datoagrupado.columns)
otras_variables.pop(otras_variables.index('MES'))
otras_variables.pop(otras_variables.index('AÑO'))
otras_variables.pop(otras_variables.index('CANTIDAD'))
otras_variables.pop(otras_variables.index('MUNICIPIO'))
otras_variables.pop(otras_variables.index('DIA'))
opcion_y=st.sidebar.selectbox(label="selecciona una variable a evaluar",options=otras_variables)



col1, col2, col3 = st.columns(3)
    

with col1:
    st.markdown(f"*Cantidad de casos :* {departamento_df.shape[0]}")
    st.markdown(f"*Tipo de arma usada:* {np.max(departamento_df['ARMAS MEDIOS'])}")
   
with col2:
    st.markdown(f"*Rango mas alto correspondiente al municipio de:*  {np.max(departamento_df['MUNICIPIO'])}")
    st.markdown(f"*Rango mas bajo correspondiente al municipio de:*  {np.min(departamento_df['MUNICIPIO'])}")

with col3:
    st.markdown(f"*Genero mas Afectado:*  {np.min(departamento_df['GENERO'])}")

col1, col2 = st.columns(2)

#Grafica de Barras
@st.cache
def plot_simple(melted_asdate: pd.DataFrame, x: pd.DataFrame, y, sales_filter: str):
    data = melted_asdate.copy()
    data = data[data["MUNICIPIO"] == sales_filter]
    fig = px.histogram(data, x=x, y=y, color=opcion_y, title=opcion_y, color_discrete_sequence=px.colors.sequential.Plasma)
    return fig, data 
plot, d = plot_simple(datoagrupado, opcion_y, "CANTIDAD",  opcion_departamento)
with col1: 
    st.plotly_chart(plot,use_container_width=True)
with col2:
    st.dataframe(d)  



st.sidebar.markdown("---")

otra_variable = list(datoagrupado.columns)
otra_variable.pop(otra_variable.index('CANTIDAD'))
otra_variable.pop(otra_variable.index('MUNICIPIO'))
otra_variable.pop(otra_variable.index('GENERO'))
otra_variable.pop(otra_variable.index('ARMAS MEDIOS'))
otra_variable.pop(otra_variable.index('GRUPO ETARIO'))
otra_variable.pop(otra_variable.index('MES'))
otra_variable.pop(otra_variable.index('DIA'))
opcion_y=st.sidebar.radio(label="",options=otra_variable)


@st.cache
def plot_simple2(melted_asdate: pd.DataFrame, x: pd.DataFrame, y, sales_filter: str):
    data = melted_asdate.copy()
    data = data[data["MUNICIPIO"] == sales_filter]
    fig = px.bar(data, x=x, y=y, color_discrete_sequence=px.colors.sequential.Blues, title=opcion_y)
    return fig, data 
plotaño, d = plot_simple2(datoagrupado, opcion_y, "CANTIDAD",  opcion_departamento)

otra_var = list(datoagrupado.columns)
otra_var.pop(otra_var.index('CANTIDAD'))
otra_var.pop(otra_var.index('MUNICIPIO'))
otra_var.pop(otra_var.index('GENERO'))
otra_var.pop(otra_var.index('ARMAS MEDIOS'))
otra_var.pop(otra_var.index('GRUPO ETARIO'))
otra_var.pop(otra_var.index('AÑO'))
otra_var.pop(otra_var.index('DIA'))
opcion_y=st.sidebar.radio(label=" ",options=otra_var)


@st.cache
def plot_simple3(melted_asdate: pd.DataFrame, x: pd.DataFrame, y, sales_filter: str):
    data = melted_asdate.copy()
    data = data[data["MUNICIPIO"] == sales_filter]
    fig = px.bar(data, x=x, y=y, color_discrete_sequence=px.colors.sequential.RdBu, title=opcion_y)
    return fig, data 
plotmes, d = plot_simple3(datoagrupado, opcion_y, "CANTIDAD",  opcion_departamento)


otra_va = list(datoagrupado.columns)
otra_va.pop(otra_va.index('CANTIDAD'))
otra_va.pop(otra_va.index('MUNICIPIO'))
otra_va.pop(otra_va.index('GENERO'))
otra_va.pop(otra_va.index('ARMAS MEDIOS'))
otra_va.pop(otra_va.index('GRUPO ETARIO'))
otra_va.pop(otra_va.index('AÑO'))
otra_va.pop(otra_va.index('MES'))

opcion_y=st.sidebar.radio(label="  ",options=otra_va)


@st.cache
def plot_simple4(melted_asdate: pd.DataFrame, x: pd.DataFrame, y, sales_filter: str):
    data = melted_asdate.copy()
    data = data[data["MUNICIPIO"] == sales_filter]
    fig = px.bar(data, x=x, y=y, color_discrete_sequence=px.colors.sequential.Plasma, title=opcion_y)
    return fig, data 
plotdia, d = plot_simple4(datoagrupado, opcion_y, "CANTIDAD",  opcion_departamento)

st.markdown("---")
st.markdown("## *Grafico general de los departamentos y municipios con base en los casos presentes*")
col1, col2,  = st.columns(2)
with col1:
    st.plotly_chart(plotdia,use_container_width=True)    
with col2:
    st.plotly_chart(plotmes,use_container_width=True)


st.plotly_chart(plotaño,use_container_width=True)

st.markdown("---")

lista_año = list(departamento_df['AÑO'].unique())
st.markdown("*Lista de casos de acuerdo al AÑO*")
opcion_año = st.selectbox(label= "selecciona un año", options= lista_año)

otra_var_año = list(datoagrupado.columns)
otra_var_año.pop(otra_var_año.index('CANTIDAD'))
otra_var_año.pop(otra_var_año.index('MUNICIPIO'))
otra_var_año.pop(otra_var_año.index('GENERO'))
otra_var_año.pop(otra_var_año.index('ARMAS MEDIOS'))
otra_var_año.pop(otra_var_año.index('GRUPO ETARIO'))
otra_var_año.pop(otra_var_año.index('AÑO'))

opcion_y=st.radio(label="     ",options=otra_var_año)


@st.cache
def plot_simple5(melted_asdate: pd.DataFrame, x: pd.DataFrame, y, sales_filter: str):
    data = melted_asdate.copy()
    data = data[data["AÑO"] == sales_filter]
    fig = px.box(data, x=x, y=y, color=opcion_y, title=f"Casos del {opcion_y}",color_discrete_sequence=px.colors.sequential.Plasma)
    
    return fig, data 
plot_date_año, d = plot_simple5(datoagrupado, opcion_y, "CANTIDAD",  opcion_año)

st.plotly_chart(plot_date_año,use_container_width=True)




col1, col2, col3 =st.columns(3)
with col1:
    otra_pie_año = list(datoagrupado.columns)
    otra_pie_año.pop(otra_pie_año.index('CANTIDAD'))
    otra_pie_año.pop(otra_pie_año.index('MUNICIPIO'))
    otra_pie_año.pop(otra_pie_año.index('GENERO'))
    otra_pie_año.pop(otra_pie_año.index('GRUPO ETARIO'))
    otra_pie_año.pop(otra_pie_año.index('AÑO'))
    otra_pie_año.pop(otra_pie_año.index('DIA'))
    otra_pie_año.pop(otra_pie_año.index('MES'))
    opcion_y=st.radio(label="",options=otra_pie_año)
    @st.cache
    def pie_simple(melted_asdate: pd.DataFrame, x: pd.DataFrame, y, añofiltro: str):
        data = melted_asdate.copy()
        data = data[data["AÑO"] == añofiltro]
        #fig = px.pie(data, values=x, names=y)
        fig = px.pie(data, values=x, names=y, color_discrete_sequence=px.colors.sequential.RdBu)
        return fig, data
    plotpie, c = pie_simple(datoagrupado, "CANTIDAD", opcion_y, opcion_año)
    st.plotly_chart(plotpie,use_container_width=True)
with col2:
    otra_pie_genero = list(datoagrupado.columns)
    otra_pie_genero.pop(otra_pie_genero.index('CANTIDAD'))
    otra_pie_genero.pop(otra_pie_genero.index('MUNICIPIO'))
    otra_pie_genero.pop(otra_pie_genero.index('ARMAS MEDIOS'))
    otra_pie_genero.pop(otra_pie_genero.index('GRUPO ETARIO'))
    otra_pie_genero.pop(otra_pie_genero.index('AÑO'))
    otra_pie_genero.pop(otra_pie_genero.index('DIA'))
    otra_pie_genero.pop(otra_pie_genero.index('MES'))
    opcion_y=st.radio(label="",options=otra_pie_genero)
    @st.cache
    def pie_simple(melted_asdate: pd.DataFrame, x: pd.DataFrame, y, generofiltro: str):
        data = melted_asdate.copy()
        data = data[data["AÑO"] == generofiltro]
        #fig = px.pie(data, values=x, names=y)
        fig = px.pie(data, values=x, names=y, color_discrete_sequence=px.colors.sequential.RdBu)
        return fig, data
    plotpiegenero, c = pie_simple(datoagrupado, "CANTIDAD", opcion_y, opcion_año)
    st.plotly_chart(plotpiegenero, use_container_width=True)
with col3:
    otra_pie_grupo = list(datoagrupado.columns)
    otra_pie_grupo.pop(otra_pie_grupo.index('CANTIDAD'))
    otra_pie_grupo.pop(otra_pie_grupo.index('MUNICIPIO'))
    otra_pie_grupo.pop(otra_pie_grupo.index('ARMAS MEDIOS'))
    otra_pie_grupo.pop(otra_pie_grupo.index('GENERO'))
    otra_pie_grupo.pop(otra_pie_grupo.index('AÑO'))
    otra_pie_grupo.pop(otra_pie_grupo.index('DIA'))
    otra_pie_grupo.pop(otra_pie_grupo.index('MES'))
    opcion_y=st.radio(label="",options=otra_pie_grupo)
    @st.cache
    def pie_simple(melted_asdate: pd.DataFrame, x: pd.DataFrame, y, generofiltro: str):
        data = melted_asdate.copy()
        data = data[data["AÑO"] == generofiltro]
        #fig = px.pie(data, values=x, names=y)
        fig = px.pie(data, values=x, names=y, color_discrete_sequence=px.colors.sequential.RdBu)
        return fig, data
    plotpiegerupo, c = pie_simple(datoagrupado, "CANTIDAD", opcion_y, opcion_año)
    st.plotly_chart(plotpiegerupo, use_container_width=True)

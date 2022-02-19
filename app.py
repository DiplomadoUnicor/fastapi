import streamlit as st
import requests
import pandas as pd
import plotly.express as px 
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# swifter para apply lambda

st.set_page_config(layout = "wide")

@st.cache
def cargar_datos():
    return pd.read_csv('Violencia.csv', dtype={'CODIGO DANE': str})
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
    st.markdown(f"*Genero mas Afectado:*  {np.max(departamento_df['GRUPO ETARIO'])}")




datos_agrupados = df[['MUNICIPIO', 'ARMAS MEDIOS','GENERO', 'GRUPO ETARIO', 'CANTIDAD']].copy()

newdf= df[['MUNICIPIO', 'ARMAS MEDIOS','GENERO', 'GRUPO ETARIO', 'CANTIDAD']].copy()
new_df_agrupado = newdf.copy()


lista_municipio = list(departamento_df['MUNICIPIO'].unique())

st.sidebar.markdown("*Lista de casos de acuerdo al municipio*")

opcion_municipio = st.sidebar.selectbox(label= "selecciona un municipio", options= lista_municipio)

st.markdown("---")
#st.dataframe(datos_agrupados[datos_agrupados['MUNICIPIO']==opcion_departamento])
otras_variables = list(datos_agrupados.columns)
otras_variables.pop(otras_variables.index('CANTIDAD'))
otras_variables.pop(otras_variables.index('MUNICIPIO'))

opcion_y=st.sidebar.selectbox(label="selecciona una variable a evaluar",options=otras_variables)

col1, col2 = st.columns(2)

#Grafica de Barras
@st.cache
def plot_simple(df: pd.DataFrame, x: pd.DataFrame, y, sales_filter: str):
    data = df.copy()
    data = data[data["MUNICIPIO"] == sales_filter]
    fig = px.histogram(data, x=x, y=y)
    return fig, data 
plot, d = plot_simple(datos_agrupados,opcion_y,  "CANTIDAD",  opcion_municipio)
st.plotly_chart(plot)
    
    
#Grafica Circular

# chart_data = pd.DataFrame(
#      np.random.randn(45, 3),
#      columns=['GENERO', 'ARMAS MEDIOS', 'GRUPO ETARIO'])

# st.line_chart(chart_data)

# def circular():
#     fig = go.Figure(
#         go.Pie(
#             labels = df,
#             values = opcion_departamento,
#             hoverinfo = "label+percent",
#             textinfo = "value"
#         )
#     )
#     return fig

# st.header("Pie chart")
# st.plotly_chart(circular)
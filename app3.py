import streamlit as st
import requests
import pandas as pd
import plotly.express as px
#756,626
st.set_page_config(layout="wide",
                   page_icon="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/800px-Python-logo-notext.svg.png",
                   page_title = "Web app")

@st.cache
def cargar_datos(filename: str):
    return pd.read_csv(filename)

datos = cargar_datos("Vehiculos.csv")
st.sidebar.markdown("---")
lista_bcpp = list(datos['Bcpp'].unique())
opcion_bcpp = st.sidebar.selectbox(label= "selecciona un Bcpp", options= lista_bcpp)
lista_potencia = list(datos['Potencia'].unique())
opcion_potencia = st.sidebar.selectbox(label= "selecciona una potencia", options= lista_potencia)
lista_Cilindraje = list(datos['Cilindraje'].unique())
opcion_Cilindraje = st.sidebar.selectbox(label= "selecciona un cilindraje", options= lista_Cilindraje)
lista_PesoCategoria = list(datos['PesoCategoria'].unique())
opcion_PesoCategoria = st.sidebar.selectbox(label= "selecciona un categoria", options= lista_PesoCategoria)
lista_Clases = list(datos['Clase'].unique())
opcion_Clases = st.sidebar.selectbox(label= "selecciona un clase", options= lista_Clases)
lista_Marcas = list(datos['Marca'].unique())
opcion_Marcas = st.sidebar.selectbox(label= "selecciona un Marca", options= lista_Marcas)

Fechas= st.sidebar.selectbox(                           
    label="Fechas",options=["1970","1971","1972","1973","1974","1975","1976","1977","1978","1979","1980","1981","1982","1983","1984","1985","1986","1987","1988","1989","1990","1991","1992","1993","1994","1995","1996","1997","1998","1999","2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018"])

request_data= [
   {
       "Bcpp": opcion_bcpp,
       "Potencia":opcion_potencia,
       "Cilindraje":opcion_Cilindraje,
       "PesoCategoria":opcion_PesoCategoria,
       "Marca":opcion_Marcas,
       "Clase":opcion_Clases,
       "Fechas":Fechas
   }
]
url_api = "https://apidiplomado.herokuapp.com/predict"
data = str(request_data).replace("'", '"')
prediccion = requests.post(url=url_api, data=data).text
col1,col2=st.columns(2)
col1.metric(
    value=f'{pd.read_json(prediccion)["precio"][0]}',
    label="Prediccion de precio de salidad para el año: ",
         )

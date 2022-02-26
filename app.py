from matplotlib.font_manager import json_dump
import streamlit as st
import pandas as pd
import plotly.express as px 
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import requests

st.set_page_config(page_title='Violencia intrafamiliar', page_icon='sources/icon1.png', layout="wide", initial_sidebar_state="auto", menu_items=None)
st.title('*Violencia intrafamiliar en Colombia*')
st.sidebar.header("*Violencia intrafamiliar*")
st.sidebar.image('sources/Digital presentation.gif')
@st.cache
def cargar_datos():
    return pd.read_csv('book.csv', dtype={'CODIGO DANE': str})
#st.header("Violencia Intrafamiliar en Colombia")

st.sidebar.markdown("---")

df=cargar_datos()
st.dataframe(df)
st.write("La familia es definida como el escenario en el cual los individuos construyen las bases para interactuar con el mundo social, aprenden a comunicarse, a respetar y comprender las normas sociales. Actualmente, el concepto de familia se ha trasformado pues el modelo imperante, compuesto por padre, madre e hijos/as, se ha resignicado, encontrando familias extensas, familias monoparentales/monomarentales, parejas del mismo sexo, entre otras. ")
st.write("La violencia, según la Organización Mundial de la Salud (OMS) se define como “el uso intencional de la fuerza o el poder físico, de hecho o como amenaza, contra uno mismo, otra persona o un grupo de comunidad, que cause o tenga muchas probabilidades de causar lesiones, muerte, daño psicológico, trastornos en el desarrollo o privaciones.”")
st.markdown("---")
melted_asdate = df.copy()

#dividamos las fechas
melted_asdate['FECHA HECHO']= pd.to_datetime(melted_asdate['FECHA HECHO'])
melted_asdate['AÑO']= melted_asdate['FECHA HECHO'].apply(lambda x: x.year)
melted_asdate['MES']= melted_asdate['FECHA HECHO'].apply(lambda x: x.month)
melted_asdate['DIA']= melted_asdate['FECHA HECHO'].apply(lambda x: x.day)
## los casos de violencia intrafamiliar en colombia con base a cada departamento
st.header("*Casos de violencia intrafamiliar en Colombia de acuerdo al Departamento*")
st.write("Los casos de violencia intrafamiliar en Colombia son alarmantes y  llegan a ser preocupantes cuando estos los podemos ver con base a los años, meses y dias del departamento o siendo mas especifico aún, en cada municipio.")
st.markdown("---")
## seleccionamos un departamento para empezar a evaluar los datos
##########################################
 # los departamentos estan agrupado de acuerdo a la cantidad
sorted_departamento = melted_asdate.groupby('DEPARTAMENTO')['CANTIDAD'].count().sort_values(ascending=True).copy().index
select_departamento =st.sidebar.selectbox('Seleccionar Departamento:', sorted_departamento[18:])
#select_departamento = []
#######################################
departamento_df = melted_asdate[melted_asdate['DEPARTAMENTO'].isin([select_departamento])].copy()
#####################################################3
#datos_agrupados = df[['MUNICIPIO', 'ARMAS MEDIOS','GENERO', 'GRUPO ETARIO', 'CANTIDAD']].copy()
## agrupamos nuestro datos de la siguiente forma
datoagrupado = melted_asdate[['MUNICIPIO', 'ARMAS MEDIOS','GENERO', 'GRUPO ETARIO','CANTIDAD','AÑO', 'MES', 'DIA']].copy()
###########################################
# listamos los municipios de acuerdo al departamento 
lista_Municipio_por_departamentos = list(departamento_df['MUNICIPIO'].unique())
opcion_municipio = st.sidebar.selectbox(label= "Selecciona un municipio", options= lista_Municipio_por_departamentos)
######################################3
# quitamos las variables que no vamos a usar de la lista 
delete_variables = list(datoagrupado.columns)
delete_variables.pop(delete_variables.index('MES'))
delete_variables.pop(delete_variables.index('AÑO'))
delete_variables.pop(delete_variables.index('CANTIDAD'))
delete_variables.pop(delete_variables.index('MUNICIPIO'))
delete_variables.pop(delete_variables.index('DIA'))
# seleccionamos las variables que nos quedan las cuales si son manipulables
opcion_y=st.sidebar.selectbox(label="Selecciona una variable a evaluar",options=delete_variables)
st.write("*Veamos los casos de cada departamento.*")
st.write("De acuerdo a los datos que se presentan a continuación, en Colombia se manifiesta que tenemos casos con base a la cantidad, empleando el tipo de arma, mostrando cual seria el municpio con mayor y menor casos, cual es el genero mas afectado y a que grupo etario corresponde.")
#############################################################################################################3
col1, col2, col3 = st.columns(3)
## mostramos la cantidad de casos de acuerdo al departamento
with col1:
    st.markdown(f"*Cantidad de casos :* {departamento_df.shape[0]}")
    # mostramos las armas que mas se usaron en ese departamento
    st.markdown(f"*Tipo de arma usada:* {np.max(departamento_df['ARMAS MEDIOS'])}")
   
with col2:
    # de acuerdo al departamento seleccionado se muestran los municipios con mayor y menor caso
    st.markdown(f"*Rango mas alto correspondiente al municipio de:*  {np.max(departamento_df['MUNICIPIO'])}")
    st.markdown(f"*Rango mas bajo correspondiente al municipio de:*  {np.min(departamento_df['MUNICIPIO'])}")

with col3:
    # mostramos el genero mas afectado y al grupo al cual pertenece
    st.markdown(f"*Genero mas Afectado:*  {np.min(departamento_df['GENERO'])}")
    st.markdown(f"*Grupo etario mas afectado:*  {np.min(departamento_df['GRUPO ETARIO'])}")

st.markdown("---")
col1, col2 = st.columns(2)

#Grafica de Barras
@st.cache
def grafico1(melted_asdate: pd.DataFrame, x: pd.DataFrame, y, sales_filter: str):
    data = melted_asdate.copy()
    data = data[data["MUNICIPIO"] == sales_filter]
    fig = px.histogram(data, x=x, y=y, color=opcion_y, title=opcion_y, color_discrete_sequence=px.colors.sequential.Plasma)
    fig.update_yaxes(title_text="CANTIDAD")
    return fig, data 
plot, d = grafico1(datoagrupado, opcion_y, "CANTIDAD",  opcion_municipio)
with col1: 
    st.plotly_chart(plot,use_container_width=True)
with col2:
    st.dataframe(d)
    ## PARA HACER USO DE ESTE CONDICIONAL SE DEBE SELECCIONAR UNA VARIABLE A EVALUAR
    st.write("")

    if opcion_y == 'GENERO':   
        st.write("Los datos de la grafica anterior nos muestran con que magnitud se presentan los casos de violencia intrafamiliar de acuerdo al genero seleccionado.")
    elif opcion_y == 'ARMAS MEDIOS':
        st.write("El uso de las armas  para agredir a mienbros de la familia es un delito condenable, el uso de estas simboliza el miedo que puede sentir una persona que puede llegar o que  es agredida.")
    elif opcion_y == 'GRUPO ETARIO':
        st.write("Normalmente se creeria que es mas facil y un poco mas aceptable ver estos casos en los  en los adultos, pero se vuelve preocupante cuando estos casos tienen datos elevados con adolecsentes y menores.")
        

otra_variable = list(datoagrupado.columns)
opcion_año= "AÑO"

#grafica general de acuerdo a los año
@st.cache
def plot_general_date(melted_asdate: pd.DataFrame, x: pd.DataFrame, y, sales_filter: str):
    data = melted_asdate.copy()
    data = data[data["MUNICIPIO"] == sales_filter]
    fig = px.histogram(data,  opcion_año,    title= f"{opcion_año}",color_discrete_sequence=px.colors.sequential.Plasma)
    fig.update_yaxes(title_text="CANTIDAD")
    # color_discrete_sequence=px.colors.sequential.Plasma,
    return fig, data 
plotaño, d = plot_general_date(datoagrupado, opcion_año, "CANTIDAD",  opcion_municipio)
##################################################################################3
otra_var = list(datoagrupado.columns)
opcion_mes="MES" 
#grafico que nos muestra los casos por meses de acuerdo al año
@st.cache
def plot_mes_data(melted_asdate: pd.DataFrame, x: pd.DataFrame, y, sales_filter: str):
    data = melted_asdate.copy()
    data = data[data["MUNICIPIO"] == sales_filter]
    fig = px.histogram(data, x=x, y=y, color_discrete_sequence=px.colors.sequential.Plasma, title=opcion_mes)
    fig.update_yaxes(title_text="CANTIDAD")
    return fig, data 
plotmes, d = plot_mes_data(datoagrupado, opcion_mes, "CANTIDAD",  opcion_municipio)
######################### grafico de aucerdo al dia 
otra_va = list(datoagrupado.columns)
opcion_dia="DIA" #st.sidebar.radio(label="  ",options=otra_va)
@st.cache
def plot_dia_date(melted_asdate: pd.DataFrame, x: pd.DataFrame, y, sales_filter: str):
    data = melted_asdate.copy()
    data = data[data["MUNICIPIO"] == sales_filter]
    fig = px.histogram(data, x=x, y=y, color_discrete_sequence=px.colors.sequential.Plasma, title=opcion_dia)
    fig.update_yaxes(title_text="CANTIDAD")
    return fig, data 
plotdia, d = plot_dia_date(datoagrupado, opcion_dia, "CANTIDAD",  opcion_municipio)
#####################################################
st.markdown("---")
st.markdown("## *Grafico general de los departamentos y municipios con base en los casos presentes*")
col1, col2,  = st.columns(2)
with col1:
    st.plotly_chart(plotdia,use_container_width=True)    
with col2:
    st.plotly_chart(plotmes,use_container_width=True)
#st.write("Colimba")

st.plotly_chart(plotaño,use_container_width=True)

st.markdown("---")
####################################################################################33
lista_año = list(departamento_df['AÑO'].unique())
st.markdown("## *Lista de casos de acuerdo al año*")
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
def plot_año(melted_asdate: pd.DataFrame, x: pd.DataFrame, y, sales_filter: str):
    data = melted_asdate.copy()
    data = data[data["AÑO"] == sales_filter]
    fig = px.histogram(data, x=x, y=y, title=f"Casos del  {opcion_y}",color_discrete_sequence=px.colors.sequential.Plasma)
    fig.update_yaxes(title_text="CANTIDAD")
    return fig, data 
plot_date_año, d = plot_año(datoagrupado, opcion_y,  "CANTIDAD",  opcion_año)

st.plotly_chart(plot_date_año,use_container_width=True)

st.write("Los graficos a continuacion nos muestra como en colombia los casos de violencia  intrafamiliar se han manifestado de acuerdo al año")

col1, col2, col3 =st.columns(3)
with col1:
    otra_pie_año = list(datoagrupado.columns)
    opcion_armas_medios= "ARMAS MEDIOS" 
    st.write(opcion_armas_medios)
    @st.cache
    def pie_armas(melted_asdate: pd.DataFrame, x: pd.DataFrame, y, añofiltro: str):
        data = melted_asdate.copy()
        data = data[data["AÑO"] == añofiltro]
        #fig = px.pie(data, values=x, names=y)
        fig = px.pie(data, values=x, names=y, color_discrete_sequence=px.colors.sequential.Plasma)
        return fig, data
    plotpie, c = pie_armas(datoagrupado, "CANTIDAD", opcion_armas_medios, opcion_año)
    st.plotly_chart(plotpie,use_container_width=True)
with col2:
    otra_pie_genero = list(datoagrupado.columns)
    opcion_genero="GENERO" 
    st.write(opcion_genero)
    @st.cache
    def pie_genero(melted_asdate: pd.DataFrame, x: pd.DataFrame, y, generofiltro: str):
        data = melted_asdate.copy()
        data = data[data["AÑO"] == generofiltro]
        #fig = px.pie(data, values=x, names=y)
        fig = px.pie(data, values=x, names=y, color_discrete_sequence=px.colors.sequential.Plasma)
        return fig, data
    plotpiegenero, c = pie_genero (datoagrupado, "CANTIDAD", opcion_genero, opcion_año)
    st.plotly_chart(plotpiegenero, use_container_width=True)
with col3:
    otra_pie_grupo = list(datoagrupado.columns)
    opcion_Getario="GRUPO ETARIO"
    st.write(opcion_Getario) 
    @st.cache
    def pie_G_etario(melted_asdate: pd.DataFrame, x: pd.DataFrame, y, generofiltro: str):
        data = melted_asdate.copy()
        data = data[data["AÑO"] == generofiltro]
        #fig = px.pie(data, values=x, names=y)
        fig = px.pie(data, values=x, names=y, color_discrete_sequence=px.colors.sequential.Plasma)
        return fig, data
    plotpiegerupo, c = pie_G_etario(datoagrupado, "CANTIDAD", opcion_Getario, opcion_año)
    st.plotly_chart(plotpiegerupo, use_container_width=True)

st.markdown("---")
st.write("A continuación seleccione los datos los cuales quiere analizar, estos datos analizados arrojaran una predicción de acuerdo a los parámetros que usted desee.")
###################################################################333
col1, col2, col3 = st.columns(3)
with col1:
    listar_armas = list(datoagrupado['ARMAS MEDIOS'].unique())
    armas = st.selectbox(label= "selecciona un ARMA", options= listar_armas)
    
    año = st.slider(
            label = "AÑO", min_value=2010, max_value=2021)
with col2:
    lista_genero = list(datoagrupado['GENERO'].unique())
    opcion_genero = st.selectbox(label= "selecciona un GENERO", options= lista_genero)
    mes = st.slider(
        label="MES", min_value=1, max_value=12, value=1
    )
with col3:
    lista_grupo = list(datoagrupado['GRUPO ETARIO'].unique())
    opcion_grupo = st.selectbox(label= "selecciona un GRUPO", options= lista_grupo)
    
    dia = st.slider(
        label="DIA", min_value=1, max_value=31, value=1
    )


request_data = [
    {
        "DEPARTAMENTO": select_departamento,
        "MUNICIPIO": opcion_municipio,
        "ARMAS_MEDIOS": armas,
        "AÑO": año,
        "MES": mes,
        "DIA": dia,
        "GENERO": opcion_genero,
        "GRUPO_ETARIO": opcion_grupo
        
    }
]
import json 
url_api = "https://apilearndiplomado.herokuapp.com/predict"
data_result = json.dumps(request_data)
prediccion = requests.post(url=url_api, data=data_result).text
st.sidebar.markdown("---")

st.metric(        
    value=f'{pd.read_json(prediccion)["CANTIDAD"][0]}%',
    label="Teniendo en cuenta la información pedida anteriormente se puede predecir el porcentaje de violencia intrafamiliar teniendo en cuenta la cantidad",
    )
    



import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
col1 =[]
@st.cache
def cargar_datos(filename: str):

    return pd.read_csv(filename)

@st.cache
def plot_heatmap(df: pd.DataFrame, x: str, y: str):
    data_heatmap = (
        df.reset_index()[[x, y, "index"]]
        .groupby([x, y])
        .count()
        .reset_index()
        .pivot(x, y, "index")
        .fillna(0)
    )
    fig = px.imshow(
        data_heatmap,
        color_continuous_scale="Blues",
        aspect="auto",
        title=f"Heatmap {x} vs {y}",
    )
    fig.update_traces(
        hovertemplate="<b><i>"
        + y
        + "</i></b>: %{y} <br><b><i>"
        + x
        + "</i></b>: %{x} <br><b><i>Conteo interacción variables</i></b>: %{z}<extra></extra>"
    )
    return fig


datos = cargar_datos("book.csv")
# Sidebar
melted_asdate = datos.copy()
melted_asdate['FECHA HECHO']= pd.to_datetime(melted_asdate['FECHA HECHO'])
melted_asdate['AÑO']= melted_asdate['FECHA HECHO'].apply(lambda x: x.year)
melted_asdate['MES']= melted_asdate['FECHA HECHO'].apply(lambda x: x.month)
melted_asdate['DIA']= melted_asdate['FECHA HECHO'].apply(lambda x: x.day)

df = melted_asdate.copy()
datoagrupado = melted_asdate[['MUNICIPIO', 'ARMAS MEDIOS','GENERO', 'GRUPO ETARIO','CANTIDAD','AÑO', 'MES', 'DIA']].copy()


st.sidebar.markdown("### **Seleccionar Departamento:**")
sorted_departamento = melted_asdate.groupby('DEPARTAMENTO')['CANTIDAD'].count().sort_values(ascending=True).copy().index
select_departamento = ['CÓRDOBA']
select_departamento.append(st.sidebar.selectbox('', sorted_departamento[18:]))
departamento_df = melted_asdate[melted_asdate['DEPARTAMENTO'].isin(select_departamento)].copy()

# lista_municipio = list(departamento_df['MUNICIPIO'].unique())
# opcion_municipio = st.sidebar.selectbox(label= "selecciona un municipio", options= lista_municipio)

# lista_armas = list(departamento_df['ARMAS MEDIOS'].unique())
# opcion_armas = st.sidebar.selectbox(label= "selecciona un ARMA", options= lista_armas)

lista_año = list(departamento_df['AÑO'].unique())
opcion_año = st.sidebar.selectbox(label= "selecciona un AÑO", options= lista_año)

# lista_mes = list(departamento_df['MES'].unique())
# opcion_mes = st.sidebar.selectbox(label= "selecciona un MES", options= lista_mes)

# lista_dia = list(departamento_df['DIA'].unique())
# opcion_dia = st.sidebar.selectbox(label= "selecciona un DIA", options= lista_dia)

# lista_genero = list(departamento_df['GENERO'].unique())
# opcion_genero = st.sidebar.selectbox(label= "selecciona un GENERO", options= lista_genero)

# lista_grupo = list(departamento_df['GRUPO ETARIO'].unique())
# opcion_grupo = st.sidebar.selectbox(label= "selecciona un GRUPO", options= lista_grupo)
st.sidebar.markdown("---")

request_data = [
    {
        "DEPARTAMENTO": select_departamento,
        # "MUNICIPIO": opcion_municipio,
        # "ARMAS_MEDIOS": opcion_armas,
        "AÑO": opcion_año,
        # "MES": opcion_mes,
        # "DIA": opcion_dia,
        # "GENERO": opcion_genero,
        # "GRUPO_ETARIO": opcion_grupo
        
    }
]

url_api = "http://127.0.0.1:8000/predict"
data = str(request_data).replace("'", '"')
prediccion = requests.post(url=url_api, data=data).text
st.sidebar.markdown("---")

st.markdown("# Bienvenido")
st.markdown("En la parte izquierda se encuentran los selectores de caracteristicas, para calcular el precio de un vehiculo en su año de salida al mercado, basado en la guia de valores fasecolda")
st.sidebar.markdown("---")

data = str(request_data).replace("'", '"')
prediccion = requests.post(url=url_api, data=data).text
st.markdown("# Bienvenido")
st.markdown("En la parte izquierda se encuentran los selectores de caracteristicas, para calcular el precio de un vehiculo en su año de salida al mercado, basado en la guia de valores fasecolda")
st.sidebar.markdown("---")
col1,col2=st.columns(2)
col1.metric(
    value=f'{pd.read_json(prediccion)["AÑO"][0]}',
    label="Prediccion de CANTIDAD de salidad para el año: ",
         )
# Main Body

st.header("Datos de referecia utilizado para la prediccion de precios")
st.markdown("---")
st.write(datos)
st.markdown("---")

st.markdown("Figura 1.")
@st.cache
def graficobarras(datos):
    
    fig = px.bar(
        datos.groupby(["DEPARTAMENTO"])
        .count()
        .reset_index()
        .sort_values(by="CANTIDAD", ascending=False),
        color_discrete_sequence=["gray","black"],
        x ="DEPARTAMENTO",
        y ="CANTIDAD"
    )
    return fig
varfig = graficobarras(datos)
st.plotly_chart( 
    varfig , 
    use_container_width=True,  
)
st.markdown("La anterior grafica nos muestra el valor por CLASE para cada vehiculos en todas sus referencias")
st.markdown("---")

departamento = st.sidebar.selectbox(
    label="DEPARTAMENTO", options=['ATLÁNTICO', 'BOYACÁ', 'CAQUETÁ', 'CASANARE', 'CUNDINAMARCA',
       'SUCRE', 'VALLE', 'HUILA', 'ANTIOQUIA', 'ARAUCA', 'BOLÍVAR',
       'CALDAS', 'CAUCA', 'CESAR', 'CHOCÓ', 'CÓRDOBA', 'MAGDALENA',
       'META', 'NARIÑO', 'NORTE DE SANTANDER', 'PUTUMAYO', 'RISARALDA',
       'SANTANDER', 'TOLIMA', 'VAUPÉS', 'GUAVIARE', 'GUAJIRA', 'QUINDÍO',
       'AMAZONAS', 'VICHADA', 'GUAINÍA', 'SAN ANDRÉS', 'NO REPORTA']
)#print(df.groupby(['Fruit'])['Sale'].agg('sum'))                 
st.markdown("Figura 2")
def graficoValor(data,s: str):
    fig = px.bar(
        datos.groupby(datos['Marca']==s)
        .sum()
        .reset_index()
        .sort_values(by='valor_modelo'),
        x = "Marca",
        y ="valor_modelo",
        color_discrete_sequence=["violet"]
    )
    return fig
varfig = graficoValor(datos,departamento)
st.plotly_chart(
    varfig, 
    use_container_width=True,  
)
st.markdown("En el anterior grafico podemos ver los valores por marcas para todas las referencias, con respecto a los otros vehiculos")
st.markdown("---")


# def graficobarras(datos):
    
#     fig = px.bar(
#         datos.groupby(["Clase"])
#         .count()
#         .reset_index()
#         .sort_values(by="CANTIDAD", ascending=False),
#         color_discrete_sequence=["gray","black"],
#         x ="Clase",
#         y ="valor_modelo"
#     )
#     return fig
# varfig = graficobarras(datos)
# st.plotly_chart( 
#     varfig , 
#     use_container_width=True,  
# )

# col1.metric(
#     value=f'{pd.read_json(prediccion)["CANTIDAD"][0]}00',
#     label="Prediccion de LA CANTIDAD de CASOS para el año: ",
#          )

# opciones1 = list(datos.columns)
# eje_x_heatmap1 = st.sidebar.selectbox(label="Heatmap X", options=opciones1)
# opciones2 = opciones1.copy()
# opciones2.pop(opciones1.index(eje_x_heatmap1))
# eje_y_heatmap1 = st.sidebar.selectbox(label="Heatmap Y", options=opciones2)

# # Main Body
# st.header("Web app para el Diplomado de Python: Ejemplo Employee Turnover")
# st.markdown("---")
# col1, col2 = st.columns(2)

# col1.metric(
#     value=f'{pd.read_json(prediccion)["CANTIDAD"][0]}',
#     label="Predicción probabilidad renuncia",
# )
# col2.write("Esto quedaría en la columna de la derecha")

# st.markdown("---")

# st.write(datos)
# scatter_1 = plot_heatmap(df=datos, x=eje_x_heatmap1, y=eje_y_heatmap1)

# col1, col2 = st.columns(2)

# col1.plotly_chart(scatter_1, use_container_width=True)

# col2.plotly_chart(
#     px.bar(
#         datos.groupby(["left", "salary"])
#         .count()
#         .reset_index()
#         .sort_values(by="satisfaction_level", ascending=False),
#         x="salary",
#         y="satisfaction_level",
#         facet_col="left",
#     ),
#     use_container_width=True,
# )
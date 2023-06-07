from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np 
import streamlit as st
from PIL import Image
import folium
from streamlit_folium import folium_static
import inflection
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title="Visão Geral", page_icon="🎲", layout="wide")

df = pd.read_csv('zomato.csv')

# ====================================================
# # FUNÇÕES DO CIENTISTAS DE DADOS JÁ PRONTAS
# ====================================================

#Preenchimento dos nomes dos países
COUNTRIES = {
  1: "India",
  14: "Australia",
  30: "Brazil",
  37: "Canada",
  94: "Indonesia",
  148: "New Zeland",
  162: "Philippines",
  166: "Qatar",
  184: "Singapure",
  189: "South Africa",
  191: "Sri Lanka",
  208: "Turkey",
  214: "United Arab Emirates",
  215: "England",
  216: "United States of America",
}
def country_name(country_id):
  return COUNTRIES[country_id]


# Criação do tipo de categoria de comida
def create_price_tye(price_range):
  if price_range == 1:
    return "cheap"
  elif price_range == 2:
    return "normal"
  elif price_range == 3:
    return "expensive"
  else:
    return "gourmet"

# Criação dos nomes das cores
COLORS = {
  "3F7E00": "darkgreen",
  "5BA829": "green",
  "9ACD32": "lightgreen",
  "CDD614": "orange",
  "FFBA00": "red",
  "CBCBC8": "darkred",
  "FF7800": "darkred",
}
def color_name(color_code):
  return COLORS[color_code]


# Renomear as colunas dos dataframes
def rename_columns(dataframe):
  df = dataframe.copy()
  title = lambda x: inflection.titleize(x)
  snakecase = lambda x: inflection.underscore(x)
  spaces = lambda x: x.replace(" ", "")
  cols_old = list(df.columns)
  cols_old = list(map(title, cols_old))
  cols_old = list(map(spaces, cols_old))
  cols_new = list(map(snakecase, cols_old))
  df.columns = cols_new
  return df

#Tirar as nans da coluna 'Cuisiness' , que são do tipo float
df1 = df.copy()

tipo_float = lambda x: type(x) is not float
linhas_selecionadas = df['Cuisines'].apply(tipo_float)
df1 = df1[linhas_selecionadas]
linhas_selecionadas = df['Rating color'].apply(tipo_float)
df1 = df1[linhas_selecionadas]


#Transformando os restaurantes em um nome só
df1["Cuisines"] = df1.loc[:, "Cuisines"].apply(lambda x: x.split(",")[0])


# Colocando os nomes dos páises de acordo com seu código
df1['Country Name'] = df1['Country Code'].apply(country_name)

#Mudando o 'price range' de numero para palavras
df1['Price level'] = df1['Price range'].apply(create_price_tye)

#Colocando o nome das cores
df1['Color name'] = df1['Rating color'].apply(color_name)

#Desfazendo as colunas alteradas (Country Code e Rating color)
df1 = df1.drop(['Country Code', 'Rating color'], axis=1)

#Renomeando as colunas
df2 = rename_columns(df1)
print(df2.columns)

df2 = df2.reset_index(drop=True)



# ======================================================================
# ======================================================================
# BARRA LATERAL
# ======================================================================
# ======================================================================

st.title('Fome Zero')


st.header('MarketPlace - Visão Cliente')
st.markdown('### Venha conferir as principais observações a respeito do programa Fome Zero')
image = Image.open('logo.png')

st.sidebar.image(image, width = 200)

st.sidebar.markdown('### Escolha os países que deseja visualizar os restaurantes')
st.sidebar.markdown('''---''')
country_options = st.sidebar.multiselect(
    'Países', 
    ['Brazil', 'England', 'Qatar', 'South Africa', 'Canada', 'Australia', 'Phillipines', 'United States of America'\
     'Singapure', 'India', 'Indonesia', 'New Zeland', 'Sri Lanka', 'Turkey'], 
    default = ['Brazil', 'England'])

df2 = df2[df2['country_name'].isin(country_options) ] 

# ==============================================================
# ==============================================================
#LAYOUT NO STREAMLIT
# ==============================================================
# ==============================================================

tab1, tab2 = st.tabs(['Visão Geral', 'Visão Geográfica'])


with tab1:
  with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
      num_restaurantes = len(df2['restaurant_id'].unique())
      col1.metric('Restaurantes', num_restaurantes)
    with col2:
      num_paises = len(df2['country_name'].unique())
      col2.metric('Países: ', num_paises)
    with col3:
      num_cities = len(df2['city'].unique())
      col3.metric('Cidades: ', num_cities)
    with col4:
           
      col4.metric('Avaliações: ', df2['votes'].sum())
    with col5:
      num_culinaria = len(df2['cuisines'].unique())
      col5.metric('Culinárias: ', num_culinaria)
  
  with tab2:
    df_aux = df2[['city', 'latitude', 'longitude' ]].groupby(['city']).median().reset_index()
    map = folium.Map()
        
    for index, location_info in df_aux.iterrows():
      folium.Marker([location_info['latitude'], location_info['longitude']], \
                    popup=location_info[['city']]).add_to(map)


    folium_static(map, width = 1024, height=600)
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

st.set_page_config(page_title="Visão Cidade", page_icon="🎲", layout="wide")
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


st.sidebar.header('MarketPlace - Visão Cliente')
st.markdown('### Venha conferir as principais observações a respeito do programa Fome Zero')
image = Image.open('logo.png')

st.sidebar.image(image, width = 200)

st.sidebar.markdown('### Escolha os países que deseja visualizar os restaurantes')
st.sidebar.markdown('''---''')
country_options = st.sidebar.multiselect(
    'Países', 
    ['Brazil', 'England', 'Qatar', 'South Africa', 'Canada', 'Australia', 'Phillipines', 'United States of America',\
     'Singapure', 'India', 'Indonesia', 'New Zeland', 'Sri Lanka', 'Turkey'], 
    default = ['Brazil', 'England'])

df2 = df2[df2['country_name'].isin(country_options) ] 

# ==============================================================
# ==============================================================
#LAYOUT NO STREAMLIT
# ==============================================================
# ==============================================================


tab1, tab2 = st.tabs(['Visão Gerencial', '_'])

with tab1:
  with st.container():
    st.markdown('#### Cidades com mais restaurantes')
    df_aux = df2[['city', 'restaurant_id']].groupby('city').count().reset_index()
    df_aux.columns = ['city', 'count']
    df_aux = df_aux.sort_values('count', ascending=False).reset_index(drop=True)
    fig = px.bar(df_aux, x = 'city', y='count')
    st.plotly_chart(fig, use_container_width = True)
  
  with st.container():
    st.markdown('#### Cidades que possuem o maior valor médio de um prato para dois')
    df_aux = df2[['average_cost_for_two', 'city']].groupby('city').max().reset_index()
    df_aux = df_aux.sort_values('average_cost_for_two', ascending=False).reset_index(drop=True)
    fig = px.bar(df_aux, x = 'city', y='average_cost_for_two')
    st.plotly_chart(fig, use_container_width=True)
  
  with st.container():
    st.markdown('#### Cidades com o maior numero de culinárias distintas')
    df_aux = df2[['cuisines', 'city']].groupby('city').count().reset_index()
    df_aux = df_aux.sort_values('cuisines', ascending=False).reset_index(drop=True)
    fig = px.bar(df_aux, x = 'city', y='cuisines')
    st.plotly_chart(fig, use_container_width=True)
  
  with st.container():
      st.markdown('#### Cidades com maior numero de restaurantes que fazem reservas')
      df_table = df2[df2['has_table_booking']==1]
      df_aux = df_table[['city', 'restaurant_id']].groupby('city').count().reset_index()
      df_aux = df_aux.sort_values('restaurant_id', ascending=False).reset_index(drop=True)
      fig = px.bar(df_aux, x = 'city', y='restaurant_id')
      st.plotly_chart(fig, use_container_width=True)

  with st.container():
      st.markdown('#### Cidades com maior numero de restaurantes com delivery')
      df_delivery = df2[df2['is_delivering_now']==1]
      df_aux = df_delivery[['city', 'restaurant_id']].groupby('city').count().reset_index()
      df_aux = df_aux.sort_values('restaurant_id', ascending=False).reset_index(drop=True)
      fig = px.bar(df_aux, x = 'city', y='restaurant_id')
      st.plotly_chart(fig, use_container_width=True)


    
  with st.container():
      st.markdown('#### Cidades com maior numero de restaurantes com pedidos online')
      df_delivery = df2[df2['has_online_delivery']==1]
      df_aux = df_delivery[['city', 'restaurant_id']].groupby('city').count().reset_index()
      df_aux = df_aux.sort_values('restaurant_id', ascending=False).reset_index(drop=True)
      fig = px.bar(df_aux, x = 'city', y='restaurant_id')
      st.plotly_chart(fig, use_container_width=True)






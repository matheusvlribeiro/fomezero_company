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

st.set_page_config(page_title="Visão País", page_icon="🎲", layout="wide")

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
        st.markdown('##### Países com mais cidades registradas')
        df_city_country = df2[['city', 'country_name']].groupby(['country_name']).nunique().reset_index()
        df_city_country = df_city_country.sort_values(by='city', ascending=False)
        #Reiniciando os indices para pegar o primeiro país
        df_city_country = df_city_country.reset_index(drop=True)
        fig = px.bar(df_city_country, x = 'country_name', y='city')
        st.plotly_chart(fig, use_container_width = True)
    
    with st.container():
      st.markdown('##### Países com mais restaurantes registrados')
      df_restaurante_country = df2[['restaurant_id', 'country_name']].groupby('country_name').nunique().reset_index()
      df_restaurante_country = df_restaurante_country.sort_values(by='restaurant_id', ascending=False).\
        reset_index(drop=True)
      fig = px.bar(df_restaurante_country, x = 'country_name', y='restaurant_id')
      st.plotly_chart(fig, use_container_width=True)
    
    with st.container():
      st.markdown('##### Países com maior quantidade de tipos de culinária')
      df_aux = df2[['cuisines', 'country_name']].groupby('country_name').nunique().reset_index()
      df_aux.columns = ['country', 'quantidade']
      df_aux = df_aux.sort_values('quantidade', ascending=False).reset_index(drop=True)
      fig = px.bar(df_aux, x = 'country', y='quantidade')
      st.plotly_chart(fig, use_container_width = True)
    
    with st.container():
      col1, col2 = st.columns(2)
      with col1:
        st.markdown('##### País com maior quantidade de restaurantes que fazem entregas ')
        df_delivery = df2[df2['has_online_delivery']==1]
        df_aux = df_delivery[['restaurant_id', 'country_name']].groupby('country_name').nunique().reset_index()
        df_aux.columns = ['country', 'quantidade']
        df_aux = df_aux.sort_values('quantidade', ascending=False)
        fig = px.bar(df_aux, x = 'country', y='quantidade')
        st.plotly_chart(fig, use_container_width = True)
      with col2:
        st.markdown('##### País com maior quantidade de restaurantes que aceitam reservas ')
        df_reserve = df2[df2['has_table_booking']==1]
        df_aux = df_reserve[['restaurant_id', 'country_name']].groupby('country_name').nunique().reset_index()
        df_aux.columns = ['country', 'quantidade']
        df_aux = df_aux.sort_values('quantidade', ascending=False).reset_index(drop=True)
        fig = px.bar(df_aux, x = 'country', y='quantidade')
        st.plotly_chart(fig, use_container_width = True)
    
    with st.container():
      col1, col2 = st.columns(2)
      with col1:
        st.markdown('##### Países com as maiores notas ')
        df_aux = df2[['country_name','aggregate_rating']].groupby('country_name').mean().reset_index()
        df_aux.columns = ['country', 'media']
        df_aux = df_aux.sort_values('media', ascending=False).reset_index(drop=True)
        fig = px.bar(df_aux, x = 'country', y='media')
        st.plotly_chart(fig, use_container_width = True)
      with col2:
        st.markdown('##### Países com as menores notas ')
        df_aux = df2[['country_name','aggregate_rating']].groupby('country_name').mean().reset_index()
        df_aux.columns = ['country', 'media']
        df_aux = df_aux.sort_values('media', ascending=True).reset_index(drop=True)
        fig = px.bar(df_aux, x = 'country', y='media')
        st.plotly_chart(fig, use_container_width = True)


        


      
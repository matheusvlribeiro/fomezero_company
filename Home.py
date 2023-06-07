import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home", 
    page_icon = "🎶", 
    layout = "wide"
)

#image_path = '/home/matheus/repos/ftc_python/ciclo_07/logo.png'
image_path = 'logo.png'
image = Image.open(image_path)
st.sidebar.image(image, width = 120)


# =======================================
# Barra Lateral
# =======================================

st.sidebar.markdown( '# Fome Zero Company' )
st.sidebar.markdown( '## The best restaurants in the World' )
st.sidebar.markdown( """---""" )

st.write("# Fome Zero Company Growth Dashboard")

st.markdown(
    """
    Growth Dashboard foi construído para acompanhar as métricas dos países e restaurantes.
    ### Comoo utilizar esse Growth Dashboard?
    - Visão Principal:
        - Visão Gerencial: Métricas gerais 
        - Visão Geográfica: Insights de geolocalização
    - Visão País:
        - Acompanhamento dos indicadores dos países
    - Visão Cidades:
        - Indicadores das principais cidades
    - Visão Restaurante: 
        - Indicadores dos restaurantes
    """)
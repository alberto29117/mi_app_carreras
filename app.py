import streamlit as st
import pandas as pd
from scraper import scrape_horse_odds
from datetime import timedelta

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Cuotas de Caballos",
    page_icon="🏇",
    layout="wide"
)

# --- FUNCIÓN CON CACHÉ ---
@st.cache_data(ttl=timedelta(minutes=30))
def get_odds_data():
    """Esta función envuelve nuestro scraper para poder cachear sus resultados."""
    return scrape_horse_odds()

# --- Título y Descripción ---
st.title('🏇 Scraper de Cuotas de Carreras')
st.markdown("Pulsa el botón para obtener las últimas cuotas de _Sporting Life_.")
st.info("Los datos se actualizan cada 30 minutos. La primera carga del día puede tardar un poco.", icon="ℹ️")

# --- Botón de Ejecución ---
if st.button('Obtener Cuotas Ahora'):
    with st.spinner('Buscando en la web... Este proceso puede tardar hasta un minuto.'):
        datos = get_odds_data()
        
        if datos:
            df = pd.DataFrame(datos)
            st.success('¡Datos obtenidos con éxito!')
            st.dataframe(df, use_container_width=True)
        else:
            st.error('No se pudieron obtener los datos. Inténtalo de nuevo más tarde.')

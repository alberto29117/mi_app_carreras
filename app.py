import streamlit as st
import pandas as pd
from scraper import scrape_horse_odds  # Importamos la función
from datetime import timedelta

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Cuotas de Caballos",
    page_icon="🏇",
    layout="wide"
)

# --- FUNCIÓN CON CACHÉ ---
# El decorador le dice a Streamlit que guarde el resultado de esta función.
# ttl=timedelta(minutes=30) significa que la caché expira y se vuelve a ejecutar a los 30 minutos.
@st.cache_data(ttl=timedelta(minutes=30))
def get_odds_data():
    """Esta función envuelve nuestro scraper para poder cachear sus resultados."""
    return scrape_horse_odds()

# --- Título y Descripción ---
st.title('🏇 Scraper de Cuotas de Carreras')
st.markdown("Pulsa el botón para obtener las últimas cuotas de _Sporting Life_.")
st.info("Los datos se actualizan cada 30 minutos gracias a la caché.", icon="ℹ️")

# --- Botón de Ejecución ---
if st.button('Obtener Cuotas Ahora'):
    # Muestra un mensaje de "cargando" mientras el scraper trabaja
    with st.spinner('Buscando en la web... La primera vez puede tardar un poco.'):
        # Llama a nuestra nueva función con caché
        datos = get_odds_data()
        
        if datos:
            # Si se obtienen datos, conviértelos a un DataFrame de Pandas
            df = pd.DataFrame(datos)
            
            st.success('¡Datos obtenidos con éxito!')
            
            # Muestra la tabla en la aplicación
            st.dataframe(df, use_container_width=True)
        else:
            # Si no se obtienen datos, muestra un error
            st.error('No se pudieron obtener los datos. El scraper no encontró información o hubo un error.')

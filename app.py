import streamlit as st
import pandas as pd
from scraper import scrape_horse_odds  # Importamos la función desde el otro archivo

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Cuotas de Caballos",
    page_icon="🏇",
    layout="wide"
)

# --- Título y Descripción ---
st.title('🏇 Scraper de Cuotas de Carreras')
st.markdown("Pulsa el botón para obtener las últimas cuotas de _Sporting Life_.")

# --- Botón de Ejecución ---
if st.button('Obtener Cuotas Ahora'):
    # Muestra un mensaje de "cargando" mientras el scraper trabaja
    with st.spinner('Buscando en la web... Este proceso puede tardar unos segundos.'):
        # Llama a la función de scraping
        datos = scrape_horse_odds()
        
        if datos:
            # Si se obtienen datos, conviértelos a un DataFrame de Pandas
            df = pd.DataFrame(datos)
            
            st.success('¡Datos obtenidos con éxito!')
            
            # Muestra la tabla en la aplicación
            st.dataframe(df, use_container_width=True)
        else:
            # Si no se obtienen datos, muestra un error
            st.error('No se pudieron obtener los datos. Inténtalo de nuevo más tarde o revisa el scraper.')

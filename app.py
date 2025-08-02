import streamlit as st
import pandas as pd
from scraper import scrape_horse_odds

# No usamos la caché para esta prueba de depuración
def get_odds_data():
    return scrape_horse_odds()

# --- Configuración de la Página ---
st.set_page_config(page_title="Debug Scraper", page_icon="⚙️", layout="wide")

# --- Título y Descripción ---
st.title('⚙️ Depuración del Scraper de Carreras')
st.markdown("Pulsa el botón para ejecutar el scraper y ver el registro de actividad.")

if st.button('Iniciar Prueba de Scraper'):
    # Obtenemos tanto los datos como los mensajes de depuración
    datos, logs = get_odds_data()
    
    # --- MOSTRAR EL REGISTRO DE DEPURACIÓN ---
    st.subheader("Registro de Actividad del Scraper")
    st.code("\n".join(logs), language='text')

    # --- MOSTRAR LOS DATOS (SI LOS HAY) ---
    if datos:
        st.subheader("Resultados Obtenidos")
        st.success('✅ ¡El scraper ha finalizado y ha obtenido datos!')
        df = pd.DataFrame(datos)
        st.dataframe(df, use_container_width=True)
    else:
        st.subheader("Resultados Obtenidos")
        st.error('❌ El scraper ha finalizado pero no ha obtenido ningún dato. Revisa el registro de arriba para ver posibles errores.')

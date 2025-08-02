import requests
from bs4 import BeautifulSoup
import time
import random

def scrape_horse_odds():
    """
    Esta función obtiene las cuotas de todos los caballos en las carreras del día
    con los selectores CSS actualizados para Agosto de 2025.
    """
    BASE_URL = "https://www.sportinglife.com"
    RACE_CARDS_URL = f"{BASE_URL}/racing/racecards"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }
    
    all_odds_data = []
    try:
        # --- NIVEL 1: OBTENER LOS ENLACES A LAS CARRERAS DEL DÍA ---
        response = requests.get(RACE_CARDS_URL, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # --- SELECTOR CORREGIDO ---
        # El enlace a cada carrera ahora está en un <a> con esta clase.
        race_links = soup.select('a.common-race-card-race-link')
        
        if not race_links:
            print("No se encontraron enlaces de carreras. Revisa el selector 'a.common-race-card-race-link'.")
            return []

        # Limito a 5 para no tardar demasiado en cada prueba. Elimina [:5] para obtener todas.
        for link in race_links[:5]:
            race_url = BASE_URL + link['href']
            time.sleep(random.uniform(1, 2))
            
            race_response = requests.get(race_url, headers=headers)
            race_soup = BeautifulSoup(race_response.text, 'html.parser')
            
            # --- NIVEL 2: DENTRO DE UNA CARRERA, EXTRAER LOS DATOS ---
            race_title_element = race_soup.select_one('h1.rp-race-header-title')
            race_title = race_title_element.text.strip() if race_title_element else "Carrera sin título"
            
            # --- SELECTOR CORREGIDO ---
            # Cada caballo está dentro de un <div> con la clase "runner-item".
            horse_entries = race_soup.select('div.runner-item')

            for horse in horse_entries:
                # --- SELECTORES CORREGIDOS ---
                # Nombre del caballo
                horse_name_element = horse.select_one('div.runner-name-value')
                # Cuota del caballo
                odds_element = horse.select_one('span.bet-price-value')
                
                if horse_name_element and odds_element:
                    all_odds_data.append({
                        "Carrera": race_title,
                        "Caballo": horse_name_element.text.strip(),
                        "Cuota": odds_element.text.strip()
                    })

    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
        return [] # Devuelve lista vacía en caso de error de red
    except Exception as e:
        print(f"Error durante el scraping: {e}")
        return all_odds_data

    return all_odds_data

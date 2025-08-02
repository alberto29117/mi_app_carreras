import requests
from bs4 import BeautifulSoup
import time
import random

def scrape_horse_odds():
    """
    Esta función obtiene las cuotas de todos los caballos en las carreras del día.
    """
    BASE_URL = "https://www.sportinglife.com"
    RACE_CARDS_URL = f"{BASE_URL}/racing/racecards"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    
    all_odds_data = []
    try:
        response = requests.get(RACE_CARDS_URL, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # OJO: Revisa que este selector siga siendo el correcto
        race_links = soup.select('a.hr-race-card-race-link')
        
        for link in race_links[:5]: # Limito a 5 carreras para el ejemplo, quita [:5] para tenerlas todas
            race_url = BASE_URL + link['href']
            time.sleep(random.uniform(1, 3))
            
            race_response = requests.get(race_url, headers=headers)
            race_soup = BeautifulSoup(race_response.text, 'html.parser')
            
            race_title = race_soup.select_one('h1.hr-race-card-race-title').text.strip() if race_soup.select_one('h1.hr-race-card-race-title') else "Carrera sin título"
            
            horse_entries = race_soup.select('div.hr-runner-card-wrapper')
            for horse in horse_entries:
                horse_name_element = horse.select_one('span.hr-runner-horse-name')
                odds_element = horse.select_one('a[data-metrics-event-name="addToBetslip"]')
                
                if horse_name_element and odds_element:
                    all_odds_data.append({
                        "Carrera": race_title,
                        "Caballo": horse_name_element.text.strip(),
                        "Cuota": odds_element.text.strip()
                    })
    except Exception as e:
        print(f"Error durante el scraping: {e}")
        # Devuelve lo que hayas podido recolectar hasta el momento del error
        return all_odds_data

    return all_odds_data

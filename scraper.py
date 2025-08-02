from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def setup_driver():
    """Configura el driver de Selenium para ejecutarse en Streamlit Cloud."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Esencial para ejecutarse en un servidor sin interfaz gráfica
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    
    # Instala y gestiona la versión correcta del chromedriver
    service = Service(ChromeDriverManager().install())
    
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def scrape_horse_odds():
    """
    Scraper rediseñado con Selenium para manejar contenido cargado con JavaScript.
    """
    driver = setup_driver()
    BASE_URL = "https://www.sportinglife.com"
    RACE_CARDS_URL = f"{BASE_URL}/racing/racecards"
    all_odds_data = []

    try:
        driver.get(RACE_CARDS_URL)
        
        # Espera explícita hasta que los enlaces de las carreras estén presentes
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.common-race-card-race-link"))
        )
        
        # Obtenemos los elementos de los enlaces
        race_elements = driver.find_elements(By.CSS_SELECTOR, "a.common-race-card-race-link")
        race_links = [elem.get_attribute('href') for elem in race_elements]

        print(f"Se encontraron {len(race_links)} carreras.")

        # Itera sobre una copia de los enlaces
        for link in race_links[:5]: # Limito a 5 para el ejemplo
            driver.get(link)
            
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.runner-item"))
            )
            
            race_title = driver.find_element(By.CSS_SELECTOR, "h1.rp-race-header-title").text
            
            horse_entries = driver.find_elements(By.CSS_SELECTOR, "div.runner-item")
            for horse in horse_entries:
                try:
                    horse_name = horse.find_element(By.CSS_SELECTOR, "div.runner-name-value").text
                    odds = horse.find_element(By.CSS_SELECTOR, "span.bet-price-value").text
                    
                    if horse_name and odds:
                        all_odds_data.append({
                            "Carrera": race_title,
                            "Caballo": horse_name,
                            "Cuota": odds
                        })
                except:
                    # Si un caballo no tiene cuota o falta un dato, lo ignoramos y continuamos
                    continue
                    
    except Exception as e:
        print(f"Ocurrió un error con Selenium: {e}")
    finally:
        # Es muy importante cerrar el navegador para liberar recursos
        driver.quit()
        
    return all_odds_data

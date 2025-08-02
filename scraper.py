from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def setup_driver():
    """Configura el driver de Selenium con opciones de optimización."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-images")
    options.page_load_strategy = 'eager'
    
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(30)
    return driver

def scrape_horse_odds():
    """Scraper optimizado que acepta cookies y devuelve datos y un registro."""
    log_messages = []
    all_odds_data = []
    driver = None

    try:
        log_messages.append("Iniciando el driver de Selenium...")
        driver = setup_driver()
        log_messages.append("Driver iniciado correctamente.")

        RACE_CARDS_URL = "https://www.sportinglife.com/racing/racecards"
        log_messages.append(f"Accediendo a la URL principal: {RACE_CARDS_URL}")
        driver.get(RACE_CARDS_URL)
        log_messages.append("Página principal cargada.")

        # --- NUEVO PASO: ACEPTAR COOKIES ---
        try:
            log_messages.append("Buscando el botón de aceptar cookies...")
            # Espera hasta 10 segundos a que el botón sea clickeable y luego haz clic
            cookie_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "ens-accept-all-button"))
            )
            cookie_button.click()
            log_messages.append("✅ Cookies aceptadas.")
            time.sleep(1) # Pequeña pausa para que la página se reajuste
        except Exception as cookie_e:
            log_messages.append("ℹ️ No se encontró el banner de cookies o ya fue aceptado. Continuando...")
        
        # --- CONTINUACIÓN DEL CÓDIGO ---
        log_messages.append("Esperando por los enlaces de las carreras...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.common-race-card-race-link"))
        )
        
        race_elements = driver.find_elements(By.CSS_SELECTOR, "a.common-race-card-race-link")
        race_links = [elem.get_attribute('href') for elem in race_elements]
        log_messages.append(f"Se encontraron {len(race_links)} carreras en total.")

        if not race_links:
            log_messages.append("ALERTA: No se encontraron enlaces de carreras. El scraper no puede continuar.")
            return [], log_messages

        target_link = race_links[0]
        log_messages.append(f"Procesando solo la primera carrera: {target_link}")
        
        driver.get(target_link)
        log_messages.append("Página de la carrera cargada. Esperando por los datos de los caballos...")

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.runner-item"))
        )
        log_messages.append("Contenedores de caballos encontrados.")

        race_title = driver.find_element(By.CSS_SELECTOR, "h1.rp-race-header-title").text
        horse_entries = driver.find_elements(By.CSS_SELECTOR, "div.runner-item")

        for horse in horse_entries:
            try:
                horse_name = horse.find_element(By.CSS_SELECTOR, "div.runner-name-value").text
                odds = horse.find_element(By.CSS_SELECTOR, "span.bet-price-value").text
                all_odds_data.append({"Carrera": race_title, "Caballo": horse_name, "Cuota": odds})
            except:
                continue
        log_messages.append(f"Procesados {len(all_odds_data)} caballos de la primera carrera.")
        
    except Exception as e:
        log_messages.append(f"ERROR CRÍTICO: Ha ocurrido una excepción: {str(e)}")
    finally:
        if driver:
            log_messages.append("Cerrando el driver de Selenium.")
            driver.quit()
        
    return all_odds_data, log_messages

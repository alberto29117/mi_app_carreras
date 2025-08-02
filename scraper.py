from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def setup_driver():
    """Configura el driver de Selenium con el modo headless mejorado."""
    options = webdriver.ChromeOptions()
    
    # --- CAMBIO CLAVE: Usar el nuevo modo headless ---
    options.add_argument("--headless=new")
    
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
    """Scraper con camuflaje y depuración de HTML."""
    log_messages = []
    all_odds_data = []
    driver = None

    try:
        log_messages.append("Iniciando el driver de Selenium (modo camuflado)...")
        driver = setup_driver()
        log_messages.append("Driver iniciado correctamente.")

        RACE_CARDS_URL = "https://www.sportinglife.com/racing/racecards"
        log_messages.append(f"Accediendo a la URL principal: {RACE_CARDS_URL}")
        driver.get(RACE_CARDS_URL)
        log_messages.append("Página principal cargada.")

        try:
            log_messages.append("Buscando el botón de aceptar cookies...")
            cookie_button = WebDriverWait(driver, 5).until( # Reducimos la espera a 5s
                EC.element_to_be_clickable((By.ID, "ens-accept-all-button"))
            )
            cookie_button.click()
            log_messages.append("✅ Cookies aceptadas.")
            time.sleep(1)
        except Exception:
            log_messages.append("ℹ️ No se encontró el banner de cookies. Continuando...")
        
        log_messages.append("Esperando por los enlaces de las carreras...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.common-race-card-race-link"))
        )
        
        race_elements = driver.find_elements(By.CSS_SELECTOR, "a.common-race-card-race-link")
        # El resto del código para procesar las carreras... (se mantiene igual)
        # ... (código omitido por brevedad, es el mismo que antes) ...
        race_links = [elem.get_attribute('href') for elem in race_elements]
        log_messages.append(f"Se encontraron {len(race_links)} carreras en total.")

        if not race_links:
            log_messages.append("ALERTA: No se encontraron enlaces de carreras.")
            return [], log_messages

        target_link = race_links[0]
        log_messages.append(f"Procesando solo la primera carrera: {target_link}")
        
        driver.get(target_link)
        log_messages.append("Página de la carrera cargada.")
        
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.runner-item")))
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
        # --- NUEVO PASO: OBTENER EL HTML EN CASO DE ERROR ---
        if driver:
            log_messages.append("\n--- CÓDIGO FUENTE DE LA PÁGINA EN EL MOMENTO DEL ERROR ---\n")
            log_messages.append(driver.page_source)
    finally:
        if driver:
            log_messages.append("Cerrando el driver de Selenium.")
            driver.quit()
        
    return all_odds_data, log_messages

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def setup_driver():
    """Configura el driver de Selenium con camuflaje."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-images")
    options.page_load_strategy = 'eager'
    
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(40) # Aumentamos un poco el tiempo de espera general
    return driver

def scrape_horse_odds():
    """Scraper final y funcional."""
    all_odds_data = []
    driver = None

    try:
        driver = setup_driver()
        RACE_CARDS_URL = "https://www.sportinglife.com/racing/racecards"
        driver.get(RACE_CARDS_URL)

        try:
            cookie_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "ens-accept-all-button"))
            )
            cookie_button.click()
            time.sleep(2)
        except Exception:
            print("No se encontró el banner de cookies. Continuando...")
        
        # Selector para la lista de carreras (funciona)
        main_page_selector = "li.MeetingSummary__LineWrapper-sc-929fd013-2 a"
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, main_page_selector))
        )
        race_elements = driver.find_elements(By.CSS_SELECTOR, main_page_selector)
        race_links = [elem.get_attribute('href') for elem in race_elements]

        # Opcional: ajusta el número de carreras a procesar aquí
        # [:5] para las primeras 5, o déjalo sin nada para procesarlas todas.
        for link in race_links[:5]:
            driver.get(link)
            
            # --- SELECTORES FINALES Y CORREGIDOS PARA LA PÁGINA DE LA CARRERA ---
            race_title_selector = "h1.hr-racecard-race-title"
            horse_container_selector = "div.hr-runner-card-wrapper"
            
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, horse_container_selector)))
            
            race_title = driver.find_element(By.CSS_SELECTOR, race_title_selector).text
            horse_entries = driver.find_elements(By.CSS_SELECTOR, horse_container_selector)

            for horse in horse_entries:
                try:
                    horse_name = horse.find_element(By.CSS_SELECTOR, "span.hr-runner-horse-name").text
                    odds = horse.find_element(By.CSS_SELECTOR, "span.hr-runner-odds-info").text
                    all_odds_data.append({"Carrera": race_title, "Caballo": horse_name, "Cuota": odds})
                except:
                    continue # Si un caballo no tiene datos, lo saltamos
                    
    except Exception as e:
        print(f"Ha ocurrido una excepción en el scraper: {str(e)}")
    finally:
        if driver:
            driver.quit()
        
    return all_odds_data

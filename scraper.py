import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def setup_driver():
    """Configura el driver indetectable."""
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    # undetected-chromedriver maneja su propio User-Agent, por lo que no es necesario añadirlo.
    
    driver = uc.Chrome(options=options, version_main=114) # Usamos una versión específica de Chrome
    driver.set_page_load_timeout(40)
    return driver

def scrape_horse_odds():
    """Scraper final usando undetected-chromedriver."""
    all_odds_data = []
    driver = None

    try:
        driver = setup_driver()
        RACE_CARDS_URL = "https://www.sportinglife.com/racing/racecards"
        driver.get(RACE_CARDS_URL)

        time.sleep(3) # Pausa inicial para que cargue cualquier script

        try:
            cookie_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "ens-accept-all-button"))
            )
            cookie_button.click()
            time.sleep(2)
        except Exception:
            print("No se encontró el banner de cookies.")
        
        main_page_selector = "li.MeetingSummary__LineWrapper-sc-929fd013-2 a"
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, main_page_selector))
        )
        race_elements = driver.find_elements(By.CSS_SELECTOR, main_page_selector)
        race_links = [elem.get_attribute('href') for elem in race_elements]

        # Quita el [:5] si quieres procesar todas las carreras del día
        for link in race_links[:5]:
            driver.get(link)
            
            horse_container_selector = "div.hr-runner-card-wrapper"
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, horse_container_selector)))
            
            race_title = driver.find_element(By.CSS_SELECTOR, "h1.hr-racecard-race-title").text
            horse_entries = driver.find_elements(By.CSS_SELECTOR, horse_container_selector)

            for horse in horse_entries:
                try:
                    horse_name = horse.find_element(By.CSS_SELECTOR, "span.hr-runner-horse-name").text
                    odds = horse.find_element(By.CSS_SELECTOR, "span.hr-runner-odds-info").text
                    all_odds_data.append({"Carrera": race_title, "Caballo": horse_name, "Cuota": odds})
                except:
                    continue
                    
    except Exception as e:
        print(f"Ha ocurrido una excepción en el scraper: {str(e)}")
    finally:
        if driver:
            driver.quit()
        
    return all_odds_data

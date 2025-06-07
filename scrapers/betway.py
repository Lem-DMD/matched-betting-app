from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_betway():
    options = Options()
    options.add_argument('--headless')  # Run in background
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--log-level=3')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.betway.co.za/sports/grp/soccer")

    time.sleep(5)

    matches = []

    try:
        events = driver.find_elements(By.CLASS_NAME, "event-card")
        for event in events[:10]:
            try:
                match_name = event.find_element(By.CLASS_NAME, "event-title").text.strip()
                odds = event.find_elements(By.CLASS_NAME, "odds")
                odds_values = [odd.text.strip() for odd in odds[:3]]
                if odds_values:
                    matches.append({"match": match_name, "odds": odds_values})
            except:
                continue
    except Exception as e:
        print("Selenium scrape failed:", e)

    driver.quit()
    return matches

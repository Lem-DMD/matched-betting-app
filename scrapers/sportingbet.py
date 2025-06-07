from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_sportingbet():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument('--log-level=3')

    matches = []

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        driver.get("https://sports.sportingbet.co.za/en/sports/soccer")
        time.sleep(6)

        events = driver.find_elements(By.CLASS_NAME, "event-row")
        for event in events[:10]:
            try:
                teams = event.find_element(By.CLASS_NAME, "participant-names").text
                odds = [o.text for o in event.find_elements(By.CLASS_NAME, "outcome-price")]
                matches.append({"match": teams, "odds": odds[:3]})
            except:
                continue

        driver.quit()
    except Exception as e:
        print("Sportingbet scraping failed:", e)

    return matches

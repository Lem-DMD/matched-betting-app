from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_lottostar():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    matches = []

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get("https://www.lottostar.co.za/sportsbook/soccer")
        time.sleep(5)

        games = driver.find_elements(By.CLASS_NAME, "event-card")
        for game in games:
            try:
                teams = game.find_element(By.CLASS_NAME, "event-title").text
                odds = [o.text for o in game.find_elements(By.CLASS_NAME, "odds")]
                if teams and len(odds) >= 2:
                    match = {
                        "match": f"{teams} (Lottostar)",
                        "home_odds": float(odds[0]),
                        "away_odds": float(odds[1]),
                        "bookmaker": "Lottostar"
                    }
                    matches.append(match)
            except:
                continue

        driver.quit()
    except Exception as e:
        print("lottostar scraping failed:", e)

    return matches

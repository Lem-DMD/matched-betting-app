from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_betcoza():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    matches = []

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get("https://www.bet.co.za/")
        time.sleep(5)

        games = driver.find_elements(By.CLASS_NAME, "event")
        for game in games:
            try:
                teams = game.find_element(By.CLASS_NAME, "event-header").text
                odds = [o.text for o in game.find_elements(By.CLASS_NAME, "price")]
                if teams and len(odds) >= 2:
                    match = {
                        "match": f"{teams} (Bet.co.za)",
                        "home_odds": float(odds[0]),
                        "away_odds": float(odds[1]),
                        "bookmaker": "Bet.co.za"
                    }
                    matches.append(match)
            except:
                continue

        driver.quit()
    except Exception as e:
        print("betcoza scraping failed:", e)

    return matches


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
    options.add_argument("--disable-dev-shm-usage")
    matches = []

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get("https://sports.sportingbet.co.za/en/sports/soccer")
        time.sleep(5)

        for _ in range(10):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        games = driver.find_elements(By.CLASS_NAME, "event-row")
        for game in games:
            try:
                teams = game.find_element(By.CLASS_NAME, "participant-names").text
                odds = [o.text for o in game.find_elements(By.CLASS_NAME, "outcome-price")]
                if teams and len(odds) >= 2:
                    match = {
                        "match": teams,
                        "home_odds": float(odds[0]),
                        "away_odds": float(odds[1]),
                        "bookmaker": "SportingBet"
                    }
                    matches.append(match)
            except:
                continue

        driver.quit()
    except Exception as e:
        print("sportingbet scraping failed:", e)

    return matches

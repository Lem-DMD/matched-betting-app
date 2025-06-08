from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_supabets():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    matches = []

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get("https://www.supabets.co.za/betting/sports/home/soccer")
        time.sleep(5)

        for _ in range(5):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        games = driver.find_elements(By.CLASS_NAME, "event")
        for game in games:
            try:
                teams = game.find_element(By.CLASS_NAME, "event-header").text
                odds = [o.text for o in game.find_elements(By.CLASS_NAME, "price")]
                if teams and len(odds) >= 2:
                    match = {
                        "match": f"{teams} (Supabets)",
                        "home_odds": float(odds[0]),
                        "away_odds": float(odds[1]),
                        "bookmaker": "Supabets"
                    }
                    matches.append(match)
            except:
                continue

        driver.quit()
    except Exception as e:
        print("supabets scraping failed:", e)

    return matches

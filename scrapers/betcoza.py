
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

        SCROLL_PAUSE = 2
        last_height = driver.execute_script("return document.body.scrollHeight")
        for _ in range(10):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        games = driver.find_elements(By.CLASS_NAME, "event")
        for game in games:
            try:
                teams = game.find_element(By.CLASS_NAME, "event-header").text
                odds = [o.text for o in game.find_elements(By.CLASS_NAME, "price")]
                if teams and odds:
                    matches.append({"match": teams, "odds": odds[:3]})
            except:
                continue

        driver.quit()
    except Exception as e:
        print("betcoza scraping failed:", e)

    return matches

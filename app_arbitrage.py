
import streamlit as st
from scrapers.betway import scrape_betway
from scrapers.supabets import scrape_supabets
from scrapers.betcoza import scrape_betcoza
from scrapers.hollywoodbets import scrape_hollywoodbets
from scrapers.sportingbet import scrape_sportingbet
from scrapers.lottostar import scrape_lottostar

from notifiers.telegram_alert import send_telegram_message

# 🔒 Replace with your actual token from BotFather
TELEGRAM_TOKEN = "7901789930:AAECXY7NaEyBL4ca493Rgszir61RQZPsSXA"
TELEGRAM_CHAT_ID = "7012660852"

st.set_page_config(page_title="SA Matched Betting Arbitrage", layout="wide")
st.title("🇿🇦 SA Matched Betting Arbitrage Tool")
st.caption("Compares odds from SA bookmakers to find profitable opportunities.")

odds_data = []

# Load all scrapers with safe error handling
with st.spinner("🔍 Fetching bookmaker odds..."):
    try:
        odds_data.extend(scrape_betway())
        st.success("✅ Betway loaded")
    except Exception as e:
        st.warning(f"⚠️ Betway failed: {e}")

    try:
        odds_data.extend(scrape_supabets())
        st.success("✅ Supabets loaded")
    except Exception as e:
        st.warning(f"⚠️ Supabets failed: {e}")

    try:
        odds_data.extend(scrape_betcoza())
        st.success("✅ Bet.co.za loaded")
    except Exception as e:
        st.warning(f"⚠️ Bet.co.za failed: {e}")

    try:
        odds_data.extend(scrape_hollywoodbets())
        st.success("✅ HollywoodBets loaded")
    except Exception as e:
        st.warning(f"⚠️ HollywoodBets failed: {e}")

    try:
        odds_data.extend(scrape_sportingbet())
        st.success("✅ Sportingbet loaded")
    except Exception as e:
        st.warning(f"⚠️ Sportingbet failed: {e}")

    try:
        odds_data.extend(scrape_lottostar())
        st.success("✅ Lottostar loaded")
    except Exception as e:
        st.warning(f"⚠️ Lottostar failed: {e}")

# Arbitrage logic
def detect_arbitrage(odds_data):
    alerts = []
    grouped = {}

    for item in odds_data:
        match = item.get("match")
        if not match or "home_odds" not in item or "away_odds" not in item:
            continue
        if match not in grouped:
            grouped[match] = []
        grouped[match].append(item)

    for match, entries in grouped.items():
        best_home = 0
        best_away = 0
        for e in entries:
            try:
                home = float(e["home_odds"])
                away = float(e["away_odds"])
                if home > best_home:
                    best_home = home
                if away > best_away:
                    best_away = away
            except:
                continue
        if best_home > 0 and best_away > 0:
            arb_percent = (1 / best_home) + (1 / best_away)
            if arb_percent < 1:
                profit = round((1 - arb_percent) * 100, 2)
                alerts.append({
                    "match": match,
                    "home_odds": best_home,
                    "away_odds": best_away,
                    "profit": profit
                })

    return alerts

alerts = detect_arbitrage(odds_data)

# Display section
st.subheader("📈 Arbitrage Opportunities")
if alerts:
    for alert in alerts:
        st.success(f"{alert['match']} | Profit: {alert['profit']}% | Home: {alert['home_odds']} | Away: {alert['away_odds']}")
        # Send Telegram alert
        msg = f"📣 Arbitrage Alert!\nMatch: {alert['match']}\nProfit: {alert['profit']}%\nHome: {alert['home_odds']}\nAway: {alert['away_odds']}"
        send_telegram_message(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, msg)
else:
    st.info("No arbitrage opportunities found.")

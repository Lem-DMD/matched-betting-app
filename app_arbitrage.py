
import streamlit as st
from scrapers.betway import scrape_betway
from scrapers.supabets import scrape_supabets
from scrapers.betcoza import scrape_betcoza
from scrapers.hollywoodbets import scrape_hollywoodbets
from scrapers.sportingbet import scrape_sportingbet
from scrapers.lottostar import scrape_lottostar

st.set_page_config(page_title="SA Matched Betting Arbitrage", layout="wide")
st.title("🇿🇦 SA Matched Betting Arbitrage Tool")
st.caption("Compares odds from 6 bookmakers to find profitable arbitrage matchups.")

odds_data = []

# Fetch odds from all bookmakers with error handling
with st.spinner("Fetching odds from bookmakers..."):
    try:
        odds_data.extend(scrape_betway())
        st.success("✅ Betway loaded")
    except Exception as e:
        st.warning(f"❌ Betway failed: {e}")

    try:
        odds_data.extend(scrape_supabets())
        st.success("✅ Supabets loaded")
    except Exception as e:
        st.warning(f"❌ Supabets failed: {e}")

    try:
        odds_data.extend(scrape_betcoza())
        st.success("✅ Bet.co.za loaded")
    except Exception as e:
        st.warning(f"❌ Bet.co.za failed: {e}")

    try:
        odds_data.extend(scrape_hollywoodbets())
        st.success("✅ Hollywoodbets loaded")
    except Exception as e:
        st.warning(f"❌ Hollywoodbets failed: {e}")

    try:
        odds_data.extend(scrape_sportingbet())
        st.success("✅ Sportingbet loaded")
    except Exception as e:
        st.warning(f"❌ Sportingbet failed: {e}")

    try:
        odds_data.extend(scrape_lottostar())
        st.success("✅ Lottostar loaded")
    except Exception as e:
        st.warning(f"❌ Lottostar failed: {e}")

# Group and detect arbitrage
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

st.subheader("📈 Arbitrage Opportunities")
if alerts:
    for alert in alerts:
        st.success(f"{alert['match']} | Profit: {alert['profit']}% | Home: {alert['home_odds']} | Away: {alert['away_odds']}")
else:
    st.info("No arbitrage opportunities found.")

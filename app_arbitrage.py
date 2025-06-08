
import streamlit as st
from scrapers.betway import scrape_betway
from scrapers.supabets import scrape_supabets
from scrapers.betcoza import scrape_betcoza
from scrapers.hollywoodbets import scrape_hollywoodbets
from scrapers.sportingbet import scrape_sportingbet
from scrapers.lottostar import scrape_lottostar

from notifiers.telegram_alert import send_telegram_message
from streamlit_autorefresh import st_autorefresh

# Telegram credentials
TELEGRAM_TOKEN = "YOUR_BOT_TOKEN"
TELEGRAM_CHAT_ID = "7012660852"

st.set_page_config(page_title="SA Matched Betting Arbitrage", layout="wide")
st_autorefresh(interval=600000, key="refresh")
st.title("🇿🇦 SA Matched Betting Arbitrage Tool")
st.caption("Compare odds across bookmakers, find arbitrage, and suggest multibet combos.")

# Filters
selected_bookmakers = st.multiselect(
    "📚 Select Bookmakers",
    ["Betway", "Supabets", "Bet.co.za", "HollywoodBets", "Sportingbet", "Lottostar"],
    default=["Betway", "Supabets", "Bet.co.za", "HollywoodBets", "Sportingbet", "Lottostar"]
)

league_filter = st.text_input("🏆 Filter by League Keyword", "")

odds_data = []

with st.spinner("Fetching bookmaker odds..."):
    try:
        odds_data.extend(scrape_betway())
    except Exception as e:
        st.warning(f"Betway failed: {e}")
    try:
        odds_data.extend(scrape_supabets())
    except Exception as e:
        st.warning(f"Supabets failed: {e}")
    try:
        odds_data.extend(scrape_betcoza())
    except Exception as e:
        st.warning(f"Bet.co.za failed: {e}")
    try:
        odds_data.extend(scrape_hollywoodbets())
    except Exception as e:
        st.warning(f"HollywoodBets failed: {e}")
    try:
        odds_data.extend(scrape_sportingbet())
    except Exception as e:
        st.warning(f"Sportingbet failed: {e}")
    try:
        odds_data.extend(scrape_lottostar())
    except Exception as e:
        st.warning(f"Lottostar failed: {e}")

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
        best_home_bk = ""
        best_away_bk = ""
        for e in entries:
            try:
                home = float(e["home_odds"])
                away = float(e["away_odds"])
                if home > best_home:
                    best_home = home
                    best_home_bk = e["bookmaker"]
                if away > best_away:
                    best_away = away
                    best_away_bk = e["bookmaker"]
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
                    "home_bookmaker": best_home_bk,
                    "away_bookmaker": best_away_bk,
                    "profit": profit
                })

    return alerts

alerts = detect_arbitrage(odds_data)

# Apply filters
filtered_alerts = []
for alert in alerts:
    if any(bk.lower() in alert["match"].lower() for bk in selected_bookmakers):
        if league_filter.lower() in alert["match"].lower():
            filtered_alerts.append(alert)

# Display results
st.subheader("📈 Arbitrage Opportunities")
if filtered_alerts:
    for alert in filtered_alerts:
        st.success(f"{alert['match']} | Profit: {alert['profit']}% | Home: {alert['home_odds']} ({alert['home_bookmaker']}) | Away: {alert['away_odds']} ({alert['away_bookmaker']})")
        msg = f"📣 Arbitrage Alert!\nMatch: {alert['match']}\nProfit: {alert['profit']}%\nHome: {alert['home_odds']} ({alert['home_bookmaker']})\nAway: {alert['away_odds']} ({alert['away_bookmaker']})"
        send_telegram_message(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, msg)
else:
    st.info("No opportunities matched your filters.")

# Multibet Suggestion (Top 3 matches with best profit)
st.subheader("🎯 Suggested Multibet Combos (Top 3 Profits)")
if filtered_alerts:
    top_matches = sorted(filtered_alerts, key=lambda x: x["profit"], reverse=True)[:3]
    for i, match in enumerate(top_matches):
        st.write(f"{i+1}. {match['match']} | Home: {match['home_odds']} | Away: {match['away_odds']}")
else:
    st.info("No multibet suggestions found.")

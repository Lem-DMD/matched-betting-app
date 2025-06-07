
import streamlit as st
from scrapers.hollywoodbets import scrape_hollywoodbets
from scrapers.lottostar import scrape_lottostar
from scrapers.betway import scrape_betway
from scrapers.supabets import scrape_supabets
from scrapers.sportingbet import scrape_sportingbet
from scrapers.betcoza import scrape_betcoza

# Optional: for future alerts
# from alerts import send_telegram_alert, send_email_alert

st.set_page_config(page_title="Matched Betting SA", layout="wide")
st.title("🇿🇦 Matched Betting Odds & Arbitrage Finder")
st.caption("Built for personal matched betting comparisons across SA bookmakers")

# Fetch odds
st.sidebar.title("Options")
if st.sidebar.button("Fetch Odds"):
    st.session_state["data"] = {
        "HollywoodBets": scrape_hollywoodbets(),
        "Lottostar": scrape_lottostar(),
        "Betway": scrape_betway(),
        "Supabets": scrape_supabets(),
        "SportingBet": scrape_sportingbet(),
        "Bet.co.za": scrape_betcoza()
    }

data = st.session_state.get("data", {})
bookmakers = list(data.keys())
selected_bookmakers = st.sidebar.multiselect("Select Bookmakers", bookmakers, default=bookmakers)

# Process matches
match_dict = {}
for name in selected_bookmakers:
    for match in data.get(name, []):
        match_name = match.get("match")
        odds = match.get("odds", [])
        if not match_name or len(odds) < 2:
            continue
        if match_name not in match_dict:
            match_dict[match_name] = []
        match_dict[match_name].append((name, odds))

# Arbitrage Detection Function
def detect_arbitrage(odds_list):
    if len(odds_list) < 2:
        return False, None
    best_home = 0
    best_away = 0
    for bookie, odds in odds_list:
        try:
            home = float(odds[0])
            away = float(odds[1])
            if home > best_home:
                best_home = home
            if away > best_away:
                best_away = away
        except:
            continue
    if best_home and best_away:
        inv = 1 / best_home + 1 / best_away
        if inv < 1:
            profit_percent = round((1 - inv) * 100, 2)
            return True, profit_percent
    return False, None

# Display Results
st.markdown("## All Matches & Arbitrage Opportunities")
for match, entries in match_dict.items():
    st.markdown(f"### {match}")
    arbitrage, profit = detect_arbitrage(entries)
    if arbitrage:
        st.success(f"🔔 Arbitrage Opportunity Detected: ~{profit}% Profit")
        # send_telegram_alert(f"Arbitrage on {match}: {profit}%")
        # send_email_alert("Arbitrage Alert", f"{match} has {profit}% opportunity")
    for bookie, odds in entries:
        st.markdown(f"- **{bookie}**: {odds}")

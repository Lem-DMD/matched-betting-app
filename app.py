
import streamlit as st
from scrapers.hollywoodbets import scrape_hollywoodbets
from scrapers.lottostar import scrape_lottostar
from scrapers.betway import scrape_betway
from scrapers.supabets import scrape_supabets
from scrapers.sportingbet import scrape_sportingbet
from scrapers.betcoza import scrape_betcoza

# Title
st.title("South Africa Matched Betting Odds Scraper")
st.markdown("Built for matched betting comparisons across multiple SA bookmakers.")

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

# Display results
data = st.session_state.get("data", {})
bookmakers = list(data.keys())

selected_bookmakers = st.sidebar.multiselect("Select Bookmakers", bookmakers, default=bookmakers)

all_matches = []
for name in selected_bookmakers:
    matches = data.get(name, [])
    for m in matches:
        match_name = m.get("match")
        odds = m.get("odds")
        if match_name and odds:
            all_matches.append({
                "bookmaker": name,
                "match": match_name,
                "odds": odds
            })

match_names = list(set(m["match"] for m in all_matches))
selected_match = st.selectbox("Choose Match to View All Bookmaker Odds", match_names)

st.markdown(f"### Odds for: {selected_match}")
for match in all_matches:
    if match["match"] == selected_match:
        st.write(f"**{match['bookmaker']}**: {match['odds']}")

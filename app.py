import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(page_title="2026 Bracket Analyzer", layout="wide", page_icon="🏀")

# Standardized Logo Helper
def get_logo_url(team_name):
    # Mapping for teams that might have different names in ESPN's API
    overrides = {
        "Miami (OH)": "miami-oh",
        "UConn": "connecticut",
        "Saint Mary's": "st-marys-ca",
    }
    slug = overrides.get(team_name, team_name.lower().replace(" ", "-").replace("st.", "state").replace(".", ""))
    return f"https://a.espncdn.com/i/teamlogos/ncaa/500/{slug}.png"

@st.cache_data
def load_data():
    summary = pd.read_csv('summary26.csv')
    miya = pd.read_csv('Evan Miya data.csv')
    # Cleanup column names
    summary.columns = summary.columns.str.replace('"', '').str.strip()
    return summary, miya

try:
    df_s, df_m = load_data()

    st.title("🏀 2026 Tournament DNA & Trend Analysis")
    st.markdown("### Selection Sunday Edition: Who fits the championship blueprint?")

    # Trend Selection
    trend = st.selectbox(
        "Choose a Historical Trend:",
        ["National Champion Profile", "Final Four Contenders", "Early Exit: Defense Risk", "Early Exit: Quarterfinal Curse"]
    )

    if "National Champion" in trend:
        st.success("🏆 **The 25/25 Rule:** Top 25 in both Offense and Defense. This is the 'Gold Standard'.")
        filtered = df_s[(df_s['RankAdjOE'] <= 25) & (df_s['RankAdjDE'] <= 25)]
        target_col, rank_col = 'TeamName', 'RankAdjEM'

    elif "Final Four" in trend:
        st.info("🔥 **The 40/40 Rule:** Balanced teams that rank in the Top 40 of both categories.")
        filtered = df_s[(df_s['RankAdjOE'] <= 40) & (df_s['RankAdjDE'] <= 40)]
        target_col, rank_col = 'TeamName', 'RankAdjEM'

    elif "Defense Risk" in trend:
        st.warning("⚠️ **Lopsided Seeds:** Top 4 seeds with a Defensive Rank worse than 50. These are 'Upset Alerts'.")
        filtered = df_m[(df_m['rank'] <= 16) & (df_m['def_rank'] > 50)]
        target_col, rank_col = 'team', 'rank'

    else:
        st.error("📉 **The Quarterfinal Curse:** High seeds that failed to reach their Conference Semifinals.")
        # Fixed 2026 list based on final results
        curse_list = ["Alabama", "Tennessee", "Kentucky", "Baylor", "Miami (OH)"]
        filtered = df_m[df_m['team'].isin(curse_list)]
        target_col, rank_col = 'team', 'rank'

    # Prepare data for display
    results = []
    for _, row in filtered.iterrows():
        team_name = row[target_col]
        results.append({
            "Logo": get_logo_url(team_name),
            "Team": team_name,
            "Overall Rank": row[rank_col],
            "Offense Rank": row['RankAdjOE'] if 'RankAdjOE' in row else row['off_rank'],
            "Defense Rank": row['RankAdjDE'] if 'RankAdjDE' in row else row['def_rank']
        })

    display_df = pd.DataFrame(results).sort_values("Overall Rank")

    # Display Table with Logos
    st.data_editor(
        display_df,
        column_config={
            "Logo": st.column_config.ImageColumn("Logo", width="small"),
            "Overall Rank": st.column_config.NumberColumn("Ovr Rank", format="#%d"),
            "Offense Rank": st.column_config.NumberColumn("Off Rank", format="#%d"),
            "Defense Rank": st.column_config.NumberColumn("Def Rank", format="#%d"),
        },
        hide_index=True,
        use_container_width=True
    )

except Exception as e:
    st.error(f"Error: {e}")

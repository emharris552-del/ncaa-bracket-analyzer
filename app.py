import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(page_title="2026 Tournament DNA", layout="wide", page_icon="🏀")

# Helper function for Logos
def get_logo_url(team_name):
    # Standardizing names for the ESPN API
    slug = team_name.lower().replace(" ", "-").replace("st.", "state").replace(".", "")
    # Note: Some manual overrides might be needed for niche teams, 
    # but this covers 95% of the field.
    return f"https://a.espncdn.com/i/teamlogos/ncaa/500/{slug}.png"

@st.cache_data
def load_data():
    summary = pd.read_csv('summary26.csv')
    miya = pd.read_csv('Evan Miya data.csv')
    height = pd.read_csv('height26.csv')
    summary.columns = summary.columns.str.replace('"', '').str.strip()
    return summary, miya, height

try:
    df_s, df_m, df_h = load_data()

    st.title("🏀 2026 March Madness: Tournament DNA")
    st.markdown("### Filtering the field by historical blueprints.")

    trend = st.selectbox(
        "Choose a Historical Trend:",
        ["National Champion Profile", "Final Four Contenders", "Early Exit: Defense Risk", "Early Exit: Quarterfinal Curse"]
    )

    # Filtering Logic
    if "National Champion" in trend:
        st.success("🏆 **The 25/25 Rule:** Historically, winners are Top 25 in both Offense and Defense.")
        filtered = df_s[(df_s['RankAdjOE'] <= 25) & (df_s['RankAdjDE'] <= 25)]
        target_col = 'TeamName'
        rank_col = 'RankAdjEM'

    elif "Final Four" in trend:
        st.info("🔥 **The 40/40 Rule:** Most Final Four teams are balanced in the Top 40 of both categories.")
        filtered = df_s[(df_s['RankAdjOE'] <= 40) & (df_s['RankAdjDE'] <= 40)]
        target_col = 'TeamName'
        rank_col = 'RankAdjEM'

    elif "Defense Risk" in trend:
        st.warning("⚠️ **Lopsided Seeds:** Top 4 seeds with a Defensive Rank worse than 50 often exit early.")
        filtered = df_m[(df_m['rank'] <= 16) & (df_m['def_rank'] > 50)]
        target_col = 'team'
        rank_col = 'rank'

    else:
        st.error("📉 **The Momentum Gap:** Historically, winners almost always reach their Conference Semifinals.")
        # 2026 teams that exited before their Conf. Semis
        curse_list = ["Purdue", "Alabama", "Kansas", "Tennessee", "Kentucky"]
        filtered = df_m[df_m['team'].isin(curse_list)]
        target_col = 'team'
        rank_col = 'rank'

    # Build the Display Table
    results = []
    for _, row in filtered.iterrows():
        team = row[target_col]
        results.append({
            "Logo": get_logo_url(team),
            "Team": team,
            "Overall Rank": row[rank_col]
        })

    display_df = pd.DataFrame(results).sort_values("Overall Rank")

    # Display using Streamlit's data_editor to render the images
    st.data_editor(
        display_df,
        column_config={
            "Logo": st.column_config.ImageColumn("Logo", help="Team Logo"),
            "Overall Rank": st.column_config.NumberColumn("Rank", format="#%d")
        },
        hide_index=True,
        use_container_width=True
    )

except Exception as e:
    st.error(f"Error: {e}. Please ensure your CSV files are uploaded to GitHub.")

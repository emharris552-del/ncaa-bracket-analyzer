import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(page_title="2026 Tournament DNA", layout="wide")

# 1. Load Data
@st.cache_data
def load_data():
    # We'll use the files you uploaded
    summary = pd.read_csv('summary26.csv')
    miya = pd.read_csv('Evan Miya data.csv')
    # Clean up column names (remove quotes if they exist)
    summary.columns = summary.columns.str.replace('"', '').str.strip()
    return summary, miya

try:
    df_summary, df_miya = load_data()

    st.title("🏀 2026 March Madness: Tournament DNA")
    st.markdown("### Analyzing the field based on historical success metrics.")

    # Create the Tab
    tab1, tab2 = st.tabs(["🏆 Historical Trends", "⚔️ Head-to-Head (Coming Soon)"])

    with tab1:
        st.header("Tournament Profile Filters")
        
        trend = st.radio(
            "Select a historical trend to analyze:",
            ["National Champion Profile", "Final Four Contenders", "Early Exit Risk"],
            horizontal=True
        )

        if trend == "National Champion Profile":
            st.info("**Trend:** Since 2002, almost every champion ranked Top 25 in both Adj. Offense and Adj. Defense.")
            # Filter logic: AdjOE Rank <= 25 and AdjDE Rank <= 25
            filtered = df_summary[(df_summary['RankAdjOE'] <= 25) & (df_summary['RankAdjDE'] <= 25)]
            
        elif trend == "Final Four Contenders":
            st.info("**Trend:** Final Four teams typically maintain a Top 40 rank in both efficiency categories.")
            filtered = df_summary[(df_summary['RankAdjOE'] <= 40) & (df_summary['RankAdjDE'] <= 40)]
            
        else:
            st.warning("**Trend:** High seeds (Top 4) with a Defensive Rank worse than 30 are historically 'Upset Prone'.")
            # Using Evan Miya data for overall Rank and Defense Rank
            filtered = df_miya[(df_miya['rank'] <= 16) & (df_miya['def_rank'] > 30)]

        # Display the Results
        st.subheader(f"Teams Matching: {trend}")
        
        # Clean up display columns
        if trend == "Early Exit Risk":
            display_df = filtered[['team', 'rank', 'off_rank', 'def_rank']].rename(columns={'rank': 'Overall Rank'})
        else:
            display_df = filtered[['TeamName', 'RankAdjEM', 'RankAdjOE', 'RankAdjDE']].rename(columns={'RankAdjEM': 'Overall Rank'})

        st.dataframe(display_df.sort_values('Overall Rank'), use_container_width=True)

except Exception as e:
    st.error(f"Error loading data: {e}")
    st.info("Make sure 'summary26.csv' and 'Evan Miya data.csv' are uploaded to your GitHub repository.")

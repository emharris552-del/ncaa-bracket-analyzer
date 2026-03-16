import streamlit as st
import pandas as pd

# Mock-up logic for Tab 1
def render_trends_tab(df):
    st.header("🏆 Tournament DNA & Trends")
    
    trend_choice = st.radio("Select Trend Filter:", ["National Champ Profile", "Final Four Profile", "Early Exit Risk"])
    
    if trend_choice == "National Champ Profile":
        # Filter: Top 25 Offense AND Top 25 Defense
        filtered_df = df[(df['off_rank'] <= 25) & (df['def_rank'] <= 25)]
        st.success("These teams meet the '25/25' historical threshold for a National Title.")
        
    elif trend_choice == "Early Exit Risk":
        # Filter: Seed 1-4 but Defense rank > 30
        filtered_df = df[(df['rank'] <= 16) & (df['def_rank'] > 30)]
        st.warning("High seeds with defensive rankings that historically lead to early exits.")

    # Display results with Rankings
    st.table(filtered_df[['team', 'rank', 'off_rank', 'def_rank']].sort_values('rank'))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from warnings import filterwarnings
filterwarnings('ignore')

st.set_page_config(page_title="Indian Premier League", page_icon="🏏")
st.title("Indian Premier League")

@st.cache_data
def load_csv(file_path):
    return pd.read_csv(file_path)

# File Upload instead of hardcoding paths
df = st.file_uploader("Upload IPL dataset (ipl.csv)", type=["csv"])
if df is not None:
    df = load_csv(df)
    # Continue with analysis...

# Sidebar for navigation
x = st.sidebar.selectbox("Pages", ["Home", "Match Analysis", "Batting Stats", "Bowling Stats", "Auction Analysis", "Batter vs Bowler"])

if x == "Home":
    st.image('https://www.pngall.com/wp-content/uploads/2017/04/Indian-Premier-League-Logo-2017.png')
    st.write("Welcome to the IPL Analytics Dashboard! Explore different analytics and insights.")

# Correct the usage of `x` instead of `bowler_stat`
if x == "Bowling Stats":
    # Assuming `season_data` is already defined earlier in your code
    stat = season_data.groupby('bowler').apply(lambda x: x[x['isWicketDelivery'] == 1]['batsman_run'].sum()).reset_index(name='best_bowling')
    stat = stat.sort_values(by='best_bowling', ascending=False).head(15)
    st.write(stat)

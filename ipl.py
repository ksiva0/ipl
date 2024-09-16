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
    df = pd.read_csv("ipl.csv")
    deliveries = pd.read_csv(r"C:\Users\sivak\New folder\data_sets\IPL_Ball_by_Ball_2008_2022.csv")
    match_data = pd.read_csv(r"C:\Users\sivak\New folder\data_sets\IPL_Matches_2008_2022.csv")
    auctions = pd.read_csv(r"C:\Users\sivak\New folder\data_sets\auction.csv")
    total_df = match_data.merge(deliveries, how="inner")
    team_mapping = {"Rising Pune Supergiant": "Rising Pune Supergiants",
                        "Kings XI Punjab": "Punjab Kings",
                        "Delhi Daredevils": "Delhi Capitals",
                        "Delhi Dardevils": "Delhi Capitals"
                        }

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

if x=="Match Analysis":
    # Example match analysis visualization (highest scores)
    st.subheader("Most Run Scores in IPL")
    highest_scores = deliveries.groupby('batter')['batsman_run'].sum().sort_values(ascending=False).head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=highest_scores.index, y=highest_scores.values)
    plt.xticks(rotation=45)
    plt.xlabel("Batsman")
    plt.ylabel("Total Runs")
    st.pyplot(plt)

       
    st.subheader("Top Wicket-Takers in IPL")
    top_wicket_takers = deliveries.groupby('bowler')['isWicketDelivery'].sum().sort_values(ascending=False).head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_wicket_takers.index, y=top_wicket_takers.values,color="#34ebcf")
    plt.xticks(rotation=45)
    plt.xlabel("Bowler")
    plt.ylabel("Total Wickets")
    st.pyplot(plt)


if x=="Batting Stats":
    seasons = total_df["Season"].unique()

    stats_by_season = {}
    for season in seasons:
        season_data = total_df[total_df["Season"] == season]
        stats_by_batter = {}

        for batter_stat in ["Most Runs", "Highest Scores", "Best Batting Average", "Best Batting Strike Rate", "Most Hundreds", "Most Fifties", "Most Fours", "Most Sixes", "Most Nineties"]:
            if batter_stat == "Most Runs":
                stats = season_data.groupby('batter')['batsman_run'].sum().reset_index().sort_values(by='batsman_run', ascending=False).head(15)
            elif batter_stat == "Highest Scores":
                stats = season_data.groupby(['ID', 'batter'])['batsman_run'].max().reset_index().sort_values(by='batsman_run', ascending=False).head(15)
            elif batter_stat == "Best Batting Average":
                stats = season_data.groupby('batter').apply(lambda x: x['batsman_run'].sum() / x['isWicketDelivery'].sum() if x['isWicketDelivery'].sum() > 0 else 0).reset_index(name='batting_avg').sort_values(by='batting_avg', ascending=False).head(15)
            elif batter_stat == "Best Batting Strike Rate":
                stats = season_data.groupby('batter').apply(lambda x: (x['batsman_run'].sum() / x['ballnumber'].sum()) * 100 if x['ballnumber'].sum() > 0 else 0).reset_index(name='batting_sr').sort_values(by='batting_sr', ascending=False).head(15)
            elif batter_stat == "Most Hundreds":
                stats = season_data.groupby('batter').apply(lambda x: (x['batsman_run'].sum() >= 100).sum()).reset_index(name='100s').sort_values(by='100s', ascending=False).head(15)
            elif batter_stat == "Most Fifties":
                stats = season_data.groupby('batter').apply(lambda x: (x['batsman_run'].sum() >= 50).sum()).reset_index(name='50s').sort_values(by='50s', ascending=False).head(15)
            elif batter_stat == "Most Fours":
                stats = season_data[season_data['batsman_run'] == 4].groupby('batter').size().reset_index(name='4s').sort_values(by='4s', ascending=False).head(15)
            elif batter_stat == "Most Sixes":
                stats = season_data[season_data['batsman_run'] == 6].groupby('batter').size().reset_index(name='6s').sort_values(by='6s', ascending=False).head(15)
            elif batter_stat == "Most Nineties":
                stats = season_data[season_data['batsman_run'] >= 90].groupby('batter').size().reset_index(name='90s').sort_values(by='90s', ascending=False).head(15)


            stats_by_batter[batter_stat] = stats

        stats_by_season[season] = stats_by_batter

    selected_season_batting = st.selectbox("Select a season (Batting)", seasons)
    selected_stat_batting = st.selectbox("Batting Statistic", list(stats_by_season[selected_season_batting].keys()))

    st.subheader(f"{selected_stat_batting} in {selected_season_batting}")
    st.table(stats_by_season[selected_season_batting][selected_stat_batting])

    # Visualization for Batting Statistic
    if selected_stat_batting == "Most Runs":
        plt.figure(figsize=(10, 6))
        plt.bar(stats_by_season[selected_season_batting][selected_stat_batting]['batter'], stats_by_season[selected_season_batting][selected_stat_batting]['batsman_run'])
        plt.xlabel('Batter')
        plt.xticks(rotation=60)
        plt.ylabel('Runs')
        plt.title('Most Runs by Batter')
        st.pyplot(plt)
    

if x=="Bowling Stats":
    seasons1 = total_df["Season"].unique()
    stats_by_season1 = {}

    for season in seasons1:
        season_data = total_df[total_df["Season"] == season]
        stats_by_bowler = {}

        for bowler_stat in ["Most Wickets", "Best Bowling Average", "Best Bowling", "Best Economy"]:
            if bowler_stat == "Most Wickets":
                stat = season_data.groupby('bowler')['isWicketDelivery'].sum().reset_index(name='wickets').sort_values(by='wickets', ascending=False).head(15)
           
            elif bowler_stat == "Best Bowling":
                stat = season_data.groupby('bowler').apply(lambda x: x[x['isWicketDelivery'] == 1]['batsman_run'].sum()).reset_index(name='best_bowling').sort_values(by='best_bowling', ascending=False).head(15)
            
                stat = season_data.groupby(['ID', 'bowler']).apply(lambda x: (x['isWicketDelivery'] == 1).sum()).reset_index(name='5_wickets').sort_values(by='5_wickets', ascending=False).head(15)
            elif bowler_stat == "Best Economy":
                stat = season_data.groupby('bowler').apply(lambda x:6* (x['batsman_run'].sum() / (x['ballnumber'].sum() / 6)) if (x['ballnumber'].sum() / 6) > 0 else 0).reset_index(name='economy').sort_values(by='economy').head(15)
            

            stats_by_bowler[bowler_stat] = stat

        stats_by_season1[season] = stats_by_bowler

    selected_season_bowling = st.selectbox("Select a season (Bowling)", seasons1)
    selected_stat_bowling = st.selectbox("Bowling Statistic", list(stats_by_season1[selected_season_bowling].keys()))

    st.subheader(f"{selected_stat_bowling} in {selected_season_bowling}")
    st.table(stats_by_season1[selected_season_bowling][selected_stat_bowling])

    # Visualization for Bowling Statistic
    if selected_stat_bowling == "Most Wickets":
        plt.figure(figsize=(10, 6))
        plt.bar(stats_by_season1[selected_season_bowling][selected_stat_bowling]['bowler'], stats_by_season1[selected_season_bowling][selected_stat_bowling]['wickets'])
        plt.xlabel('Bowler')
        plt.ylabel('Wickets')
        plt.xticks(rotation=45)
        plt.title('Most Wickets by Bowler')
        st.pyplot(plt)
    elif selected_stat_bowling == "Best Bowling Average":
        plt.figure(figsize=(10, 6))
        plt.bar(stats_by_season1[selected_season_bowling][selected_stat_bowling]['bowler'], stats_by_season1[selected_season_bowling][selected_stat_bowling][season_data.groupby('bowler')['isWicketDelivery'].sum().reset_index(name='wickets').sort_values(by='wickets', ascending=False).head(15)])
        plt.xlabel('Bowler')
        plt.ylabel('Wickets')
        plt.title("Best Bowling Average")
        st.pyplot(plt)



if x=="Auction Analysis":
    #st.image(r"C:\Users\pavan\Downloads\ipl-auction-generic_1702909024062_1702909030819.jpg")# Filter auction data for IPL seasons 2013 to 2023
    team_mapping = {"Rising Pune Supergiant": "Rising Pune Supergiants",
                    "Kings XI Punjab": "Punjab Kings",
                    "Delhi Daredevils": "Delhi Capitals",
                    "Delhi Dardevils": "Delhi Capitals"
                    }

    # Rename team names using replace()
    auctions['Team'] = auctions['Team'].replace(team_mapping)
    # Display raw data or additional analysis as needed
    st.write(auctions)  # Display raw data
    filtered_auction_data = auctions[(auctions['Year'] >= 2013) & (auctions['Year'] <= 2023)]

    # Convert 'Winning bid' column to numeric if needed
    filtered_auction_data['Winning bid'] = pd.to_numeric(filtered_auction_data['Winning bid'], errors='coerce')

    # Calculate average auction prices per year for each player
    avg_prices = filtered_auction_data.groupby(['Year', 'Player'])['Winning bid'].mean().reset_index()

    

    # Visualization - Bar chart for total spending per year
    total_spending = filtered_auction_data.groupby('Year')['Winning bid'].sum().reset_index()
    fig_total_spending = px.bar(total_spending, x='Year', y='Winning bid', color='Year',
                                labels={'x': 'Year', 'y': 'Total Spending'},
                                title='Total Spending in IPL Auctions per Year')
    st.plotly_chart(fig_total_spending)

    # Analysis 1: Team Spending Analysis
    st.subheader('Total Team Spending Analysis')
    team_spending = filtered_auction_data.groupby('Team')['Winning bid'].sum().sort_values(ascending=False)
    st.bar_chart(team_spending,color='#52f280')

    # Analysis 2: Player Price Distribution
    plt.figure(figsize=(8, 6))
    plt.hist(filtered_auction_data['Winning bid'], bins=20, color='skyblue', edgecolor='black')
    plt.title('Player Price Distribution')
    plt.xlabel('Winning Bid (in Crores)')
    plt.ylabel('Frequency')
    plt.grid(axis='y', alpha=0.75)
    st.pyplot(plt)

    # Convert 'Winning bid' and 'Base price' columns to numeric if needed
    filtered_auction_data['Winning bid'] = pd.to_numeric(filtered_auction_data['Winning bid'], errors='coerce')
    filtered_auction_data['Base price'] = pd.to_numeric(filtered_auction_data['Base price'], errors='coerce')

    # Calculate profit
    filtered_auction_data['Profit'] = filtered_auction_data['Winning bid'] - filtered_auction_data['Base price']

    # Visualization - Bar chart for top performing players based on profit
    st.subheader("Top performing players based on profit")
    top_players_profit = filtered_auction_data.groupby('Player')['Profit'].mean().nlargest(10)
    st.bar_chart(top_players_profit,color='#f79a05')
if x=="battervsbowler":
    data = pd.read_csv(r"C:\Users\sivak\New folder\data_sets\IPL_Ball_by_Ball_2008_2022.csv")
    batsmen = data["batter"].unique()
    bowlers = data["bowler"].unique()
    
    
    st.header("batter vs bowler")
    cols1, cols2 = st.columns([2, 2])
    with cols1:
        batsman_player = st.selectbox("Select a batsman:", batsmen)
    with cols2:
        bowler_player = st.selectbox("Select a bowler:", bowlers)
    

    filtered_data = data[(data['batter'] == batsman_player) & (data['bowler'] == bowler_player)]
    wickets_data = data[(data['batter'] == batsman_player) & (data['bowler'] == bowler_player) & (data['kind'].notnull())]

    
    total_wickets = len(wickets_data)

    
    balls_bowled = len(filtered_data)
    total_runs = filtered_data['batsman_run'].sum()
    strike_rate = round((total_runs / balls_bowled) * 100, 2)
    total_runs_scored = filtered_data['batsman_run'].sum()
    total_dot_balls = len(filtered_data[filtered_data['total_run'] == 0])


    cols1, cols2= st.columns([2, 2])
    with cols1:
        st.subheader("runs scored")
        st.metric("runs scored",total_runs_scored)
        st.subheader("strike rate")
        st.metric("SR", strike_rate)
        st.subheader("dot balls")
        st.metric("dot balls",total_dot_balls)
    with cols2:
        st.subheader("Balls  Bowled")
        st.metric("Balls Bowled", balls_bowled)
        st.subheader("wickets")
        st.metric("wickets",total_wickets)

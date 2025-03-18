import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load datasets
@st.cache_data
def load_data():
    match_info = pd.read_csv("match_info_data.csv")
    match_info['date'] = pd.to_datetime(match_info['date'])
    return match_info

df = load_data()
# Title
st.title("IPL Data Analysis Dashboard")
# Season Analysis
def seasonf():
    # Matches per season
    st.subheader("Matches Played Per Season")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.countplot(x=df['season'], palette="viridis", ax=ax)
    ax.set_xlabel("Season", fontsize=12)
    ax.set_ylabel("Matches Played", fontsize=12)
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    st.pyplot(fig)

    # Toss decisions
    st.subheader("Toss Decisions")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(x=df['toss_decision'], palette="Set2", ax=ax)
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    st.pyplot(fig)

    # Most common venues
    st.subheader("Top 10 IPL Venues")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.countplot(y=df['venue'], order=df['venue'].value_counts().index[:10], palette="magma", ax=ax)
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    st.pyplot(fig)

    # Venue & Toss Impact
    st.subheader("Venue & Toss Impact Study")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.countplot(y=df['venue'], hue=df['toss_decision'], order=df['venue'].value_counts().index[:10], palette="magma", ax=ax)
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    st.pyplot(fig)

# Team Analysis
def teamf():
    st.subheader("Most Successful Teams")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.countplot(y=df['winner'], order=df['winner'].value_counts().index, palette="coolwarm", ax=ax)
    ax.set_xlabel("Number of Wins", fontsize=12)
    ax.set_ylabel("Teams", fontsize=12)
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    st.pyplot(fig)

    # Win percentage by batting first vs chasing
    st.subheader("Win Trends - Batting First vs Chasing")
    df['win_by'] = df['win_by_runs'].apply(lambda x: 'Batting First' if x > 0 else 'Chasing')
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(x=df['win_by'], palette="Set2", ax=ax)
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    st.pyplot(fig)

    # Head-to-Head Comparison
    
    teams = sorted(df['winner'].dropna().unique())
    season = st.sidebar.selectbox("Select Season", sorted(df['season'].unique()))
    team = st.sidebar.selectbox("Select Team", teams)
    st.subheader("Head-to-Head Team Comparison")
    team1 = st.selectbox("Select Team 1", sorted(teams, reverse=True), index=7)
    team2 = st.selectbox("Select Team 2", sorted(teams))

    df_h2h = df[(df['team1'] == team1) & (df['team2'] == team2) | (df['team1'] == team2) & (df['team2'] == team1)]
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(y=df_h2h['winner'], order=df_h2h['winner'].value_counts().index, palette="coolwarm", ax=ax)
    ax.set_xlabel("Number of Wins", fontsize=12)
    ax.set_ylabel("Teams", fontsize=12)
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    st.pyplot(fig)

    # Player Performance
    st.subheader("Top Players by Runs and Wickets")
    if 'player_of_match' in df.columns:
        top_players = df['player_of_match'].value_counts().head(10)
        st.bar_chart(top_players)

# Sidebar Filters
st.sidebar.title("Ask")

st.subheader("Choose one from the below titles:")
choice = st.sidebar.radio("", ("Season Analysis", "Team Analysis"))
if choice == "Season Analysis":
    seasonf()

if choice == "Team Analysis":
    teamf()
# df_season = df[df['season'] == season]
# df_team = df[df['winner'] == team]








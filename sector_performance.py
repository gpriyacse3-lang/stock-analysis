import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import os

SECTOR_FILE = "data/sector.csv"

@st.cache_data
def load_sector_data():
    """
    Load sector mapping CSV. If not found, return empty DataFrame.
    """
    if not os.path.exists(SECTOR_FILE):
        st.warning("⚠️ Sector file not found. Sector analysis will be disabled.")
        return pd.DataFrame(columns=["ticker", "sector"])
    sector_df = pd.read_csv(SECTOR_FILE)
    sector_df.columns = sector_df.columns.str.strip().str.lower()
    return sector_df

def calculate_sector_performance(df, sector_df):
    """
    Merge stock data with sector info and calculate average yearly return per sector.
    Returns a Pandas Series sorted by performance.
    """
    if "daily_return" not in df.columns:
        df["daily_return"] = df.groupby("ticker")["close"].pct_change()

    merged = df.merge(sector_df, on="ticker", how="left")

    yearly_return = merged.groupby("ticker")["daily_return"].apply(lambda x: (1 + x).prod() - 1).reset_index()
    merged = yearly_return.merge(sector_df, on="ticker", how="left")
    sector_perf = merged.groupby("sector")["daily_return"].mean().sort_values(ascending=False)
    return sector_perf

def plot_sector_performance(df, sector_df):
    """
    Plot average yearly return by sector.
    """
    sector_perf = calculate_sector_performance(df, sector_df)

    plt.figure(figsize=(10,6))
    sector_perf.plot(kind="bar", color="skyblue")
    plt.title("Average Yearly Return by Sector")
    plt.ylabel("Average Yearly Return")
    plt.xlabel("Sector")
    plt.xticks(rotation=45)
    st.pyplot(plt)





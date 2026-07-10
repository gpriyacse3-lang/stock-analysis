import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

DATA_FILE = "master_csv.csv"
SECTOR_FILE = "sector.csv"


def load_data():
    df = pd.read_csv(DATA_FILE)
    df.columns = df.columns.str.strip().str.lower()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df

@st.cache_data
def load_sector_data():
    sector_df = pd.read_csv(SECTOR_FILE)
    sector_df.columns = sector_df.columns.str.strip().str.lower()
    return sector_df


def yearly_returns(df):
    df["daily_return"] = df.groupby("ticker")["close"].pct_change()
    yearly_return = df.groupby("ticker")["daily_return"].apply(lambda x: (1 + x).prod() - 1)
    return yearly_return.sort_values(ascending=False)


def plot_volatility(df, top_n=10):
    df["daily_return"] = df.groupby("ticker")["close"].pct_change()
    volatility = df.groupby("ticker")["daily_return"].std().sort_values(ascending=False)
    plt.figure(figsize=(10,6))
    volatility.head(top_n).plot(kind="bar", color="orange")
    plt.title(f"Top {top_n} Most Volatile Stocks")
    st.pyplot(plt)

def plot_cumulative_returns(df, top_n=5):
    df["daily_return"] = df.groupby("ticker")["close"].pct_change()
    df["cumulative_return"] = df.groupby("ticker")["daily_return"].cumsum()
    top_cumulative = df.groupby("ticker")["cumulative_return"].last().sort_values(ascending=False).head(top_n)

    plt.figure(figsize=(10,6))
    for symbol in top_cumulative.index:
        subset = df[df["ticker"] == symbol]
        plt.plot(subset["date"], subset["cumulative_return"], label=symbol)
    plt.title(f"Cumulative Return of Top {top_n} Stocks")
    plt.legend()
    st.pyplot(plt)


def plot_correlation(df):
    pivot_df = df.pivot(index="date", columns="ticker", values="close")
    corr_matrix = pivot_df.pct_change().corr()
    plt.figure(figsize=(12,8))
    sns.heatmap(corr_matrix, cmap="coolwarm", center=0)
    plt.title("Stock Price Correlation Heatmap")
    st.pyplot(plt)


def plot_correlation_bar(df, base_ticker):
    pivot_df = df.pivot(index="date", columns="ticker", values="close")
    corr_matrix = pivot_df.pct_change().corr()
    correlations = corr_matrix[base_ticker].drop(base_ticker).sort_values(ascending=False)

    plt.figure(figsize=(10,6))
    correlations.plot(kind="bar", color="skyblue")
    plt.title(f"Correlation of {base_ticker} with Other Stocks")
    st.pyplot(plt)


def plot_sector_performance(df, sector_df):
    df = df.merge(sector_df, on="ticker", how="left")
    df["daily_return"] = df.groupby("ticker")["close"].pct_change()
    yearly_return = df.groupby("ticker")["daily_return"].apply(lambda x: (1 + x).prod() - 1).reset_index()
    merged = yearly_return.merge(sector_df, on="ticker", how="left")
    sector_perf = merged.groupby("sector")["daily_return"].mean().sort_values(ascending=False)

    plt.figure(figsize=(10,6))
    sector_perf.plot(kind="bar", color="purple")
    plt.title("Average Yearly Return by Sector")
    st.pyplot(plt)

def calculate_monthly_returns(df):
    df["daily_return"] = df.groupby("ticker")["close"].pct_change()
    df["month"] = df["date"].dt.to_period("M")
    monthly_returns = df.groupby(["ticker", "month"])["daily_return"].apply(lambda x: (1 + x).prod() - 1).reset_index()
    monthly_returns.rename(columns={"daily_return": "monthly_return"}, inplace=True)
    return monthly_returns

def plot_monthly_gainers_losers(monthly_returns, month, top_n=5):
    month_data = monthly_returns[monthly_returns["month"] == month]
    gainers = month_data.sort_values(by="monthly_return", ascending=False).head(top_n)
    losers = month_data.sort_values(by="monthly_return", ascending=True).head(top_n)

    fig, axes = plt.subplots(1, 2, figsize=(14,6))
    axes[0].bar(gainers["ticker"], gainers["monthly_return"], color="green")
    axes[0].set_title(f"Top {top_n} Gainers - {month}")
    axes[1].bar(losers["ticker"], losers["monthly_return"], color="red")
    axes[1].set_title(f"Top {top_n} Losers - {month}")
    st.pyplot(fig)

def main():
    st.title("📊 Stock Analysis Dashboard")

    df = load_data()
    sector_df = load_sector_data()
    st.success("✅ Data loaded successfully")

    option = st.sidebar.selectbox(
        "Choose Analysis",
        ["Yearly Returns", "Volatility", "Cumulative Returns", "Correlation Heatmap", "Correlation Bar Chart", "Sector Performance", "Monthly Gainers/Losers"]
    )

    if option == "Yearly Returns":
        yr = yearly_returns(df)
        st.write("Top 10 Gainers")
        st.dataframe(yr.head(10))
        st.write("Top 10 Losers")
        st.dataframe(yr.tail(10))

    elif option == "Volatility":
        plot_volatility(df)

    elif option == "Cumulative Returns":
        plot_cumulative_returns(df)

    elif option == "Correlation Heatmap":
        plot_correlation(df)

    elif option == "Correlation Bar Chart":
        base_ticker = st.selectbox("Select Base Ticker", df["ticker"].unique())
        plot_correlation_bar(df, base_ticker)

    elif option == "Sector Performance":
        plot_sector_performance(df, sector_df)

    elif option == "Monthly Gainers/Losers":
        monthly_returns = calculate_monthly_returns(df)
        month = st.selectbox("Select Month", monthly_returns["month"].unique().astype(str))
        plot_monthly_gainers_losers(monthly_returns, month)

if __name__ == "__main__":
    main()

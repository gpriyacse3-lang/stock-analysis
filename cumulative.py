import matplotlib.pyplot as plt

def calculate_cumulative_returns(df):
    """
    Calculate cumulative returns for each stock.
    Returns a DataFrame with cumulative returns per symbol over time.
    """
    if "Daily_Return" not in df.columns:
        df["Daily_Return"] = df.groupby("ticker")["close"].pct_change()
    df["Cumulative_Return"] = df.groupby("ticker")["Daily_Return"].cumsum()
    return df

def plot_cumulative_returns(df, top_n=5):
    """
    Plot cumulative returns for the top N performing stocks.
    """
    df = calculate_cumulative_returns(df)
    top_cumulative = (
        df.groupby("ticker")["Cumulative_Return"]
        .last()
        .sort_values(ascending=False)
        .head(top_n)
    )

    plt.figure(figsize=(10,6))
    for symbol in top_cumulative.index:
        subset = df[df["ticker"] == symbol]
        plt.plot(subset["date"], subset["Cumulative_Return"], label=symbol)

    plt.title(f"Cumulative Return of Top {top_n} Stocks")
    plt.xlabel("date")
    plt.ylabel("Cumulative Return")
    plt.legend()
    plt.show()

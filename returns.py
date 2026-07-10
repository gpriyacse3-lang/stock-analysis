
import matplotlib.pyplot as plt

def yearly_returns(df):
    """
    Calculate yearly returns for each stock.
    Returns a Pandas Series sorted by performance (best to worst).
    """
    if "Daily_Return" not in df.columns:
        df["Daily_Return"] = df.groupby("ticker")["close"].pct_change()
    yearly_return = df.groupby("ticker")["Daily_Return"].sum().sort_values(ascending=False)
    return yearly_return

def plot_cumulative_returns(df, top_n=5):
    """
    Plot cumulative returns for the top N performing stocks.
    """
    if "Daily_Return" not in df.columns:
        df["Daily_Return"] = df.groupby("ticker")["close"].pct_change()

    df["Cumulative_Return"] = df.groupby("ticker")["Daily_Return"].cumsum()
    top_cumulative = (
        df.groupby("ticker")["Cumulative_Return"]
        .last()
        .sort_values(ascending=False)
        .head(top_n)
    )

    plt.figure(figsize=(10,6))
    for symbol in top_cumulative.index:
        subset = df[df["ticker"] == symbol]
        plt.plot(subset["Date"], subset["Cumulative_Return"], label=symbol)

    plt.title(f"Cumulative Return of Top {top_n} Stocks")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.legend()
    plt.show()

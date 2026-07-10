import matplotlib.pyplot as plt

def calculate_volatility(df):
    """
    Calculate volatility (standard deviation of daily returns) for each stock.
    Returns a sorted Series with highest volatility first.
    """
    if "Daily_Return" not in df.columns:
        df["Daily_Return"] = df.groupby("ticker")["close"].pct_change()
    volatility = df.groupby("ticker")["Daily_Return"].std().sort_values(ascending=False)
    return volatility

def plot_volatility(df, top_n=10):
    """
    Plot a bar chart of the top N most volatile stocks.
    """
    volatility = calculate_volatility(df)
    plt.figure(figsize=(10,6))
    volatility.head(top_n).plot(kind="bar", color="orange")
    plt.title(f"Top {top_n} Most Volatile Stocks")
    plt.ylabel("Volatility (Std Dev of Returns)")
    plt.xlabel("Stock ticker")
    plt.show()



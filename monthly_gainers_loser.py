import matplotlib.pyplot as plt

def calculate_monthly_returns(df):
    """
    Calculate monthly returns for each stock.
    Returns a DataFrame with Symbol, Month, and Monthly_Return.
    """
    if "Daily_Return" not in df.columns:
        df["Daily_Return"] = df.groupby("ticker")["close"].pct_change()

    df["Month"] = df["date"].dt.to_period("M")

    monthly_returns = (
        df.groupby(["ticker", "Month"])["Daily_Return"]
        .sum()
        .reset_index()
        .sort_values(by=["Month", "Monthly_Return"], ascending=[True, False])
    )
    monthly_returns.rename(columns={"Daily_Return": "Monthly_Return"}, inplace=True)
    return monthly_returns

def top_monthly_gainers_losers(monthly_returns, month, top_n=5):
    """
    Get top N gainers and losers for a given month.
    """
    month_data = monthly_returns[monthly_returns["Month"] == month]
    gainers = month_data.sort_values(by="Monthly_Return", ascending=False).head(top_n)
    losers = month_data.sort_values(by="Monthly_Return", ascending=True).head(top_n)
    return gainers, losers

def plot_monthly_gainers_losers(monthly_returns, month, top_n=5):
    """
    Plot bar charts of top N gainers and losers for a given month.
    """
    gainers, losers = top_monthly_gainers_losers(monthly_returns, month, top_n)

    fig, axes = plt.subplots(1, 2, figsize=(14,6))

  
    axes[0].bar(gainers["ticker"], gainers["Monthly_Return"], color="green")
    axes[0].set_title(f"Top {top_n} Gainers - {month}")
    axes[0].set_ylabel("Monthly Return")
    axes[0].set_xlabel("ticker")

  
    axes[1].bar(losers["ticker"], losers["Monthly_Return"], color="red")
    axes[1].set_title(f"Top {top_n} Losers - {month}")
    axes[1].set_ylabel("Monthly Return")
    axes[1].set_xlabel("ticker")

    plt.tight_layout()
    plt.show()

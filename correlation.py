import seaborn as sns
import matplotlib.pyplot as plt

def calculate_correlation(df):
    """
    Calculate correlation matrix of stock closing prices.
    Returns a Pandas DataFrame with correlation coefficients.
    """
    pivot_df = df.pivot(index="date", columns="ticker", values="close")
    corr_matrix = pivot_df.pct_change().corr()
    return corr_matrix

def plot_correlation(df):
    """
    Plot a heatmap of stock price correlations.
    """
    corr_matrix = calculate_correlation(df)
    plt.figure(figsize=(12,8))
    sns.heatmap(corr_matrix, cmap="coolwarm", center=0)
    plt.title("Stock Price Correlation Heatmap")
    plt.show()

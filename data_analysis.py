from load_data import load_data
from returns import yearly_returns
from volatility import plot_volatility
from cumulative import plot_cumulative_returns
from correlation import plot_correlation

def main():
  
    df = load_data()
    print("✅ Data loaded successfully")
    print(df.head())


    print("\n📊 Calculating yearly returns...")
    yr = yearly_returns(df)

    print("\n🏆 Top 10 Gainers:\n", yr.head(10))
    print("\n📉 Top 10 Losers:\n", yr.tail(10))

    print("\n📊 Plotting volatility...")
    plot_volatility(df, top_n=10)

    print("\n📊 Plotting cumulative returns...")
    plot_cumulative_returns(df, top_n=5)

    print("\n📊 Plotting correlation heatmap...")
    plot_correlation(df)

if __name__ == "__main__":
    main()




import os
import pandas as pd

def load_stock_data(data_folder="stock_data_csv"):
    stock_data = {}
    for file in os.listdir(data_folder):
        if file.endswith(".csv"):
            ticker = file.replace(".csv", "")
            df = pd.read_csv(os.path.join(data_folder, file))
            df['date'] = pd.to_datetime(df['date'])
            df.sort_values('date', inplace=True)
            df['daily_return'] = df['close'].pct_change()
            stock_data[ticker] = df
    return stock_data


if __name__ == "__main__":
    stock_data = load_stock_data()
    print(f"Loaded {len(stock_data)} tickers")



import pandas as pd

stock_df = pd.read_csv("master_csv.csv")

sector_df = pd.read_csv("sector.csv")


merged_df = stock_df.merge(sector_df, left_on="ticker", right_on="ticker")

merged_df.to_csv("master_csv.csv_with_sector.csv", index=False)




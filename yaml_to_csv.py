import os
import yaml
import pandas as pd


INPUT_DIR = "data_yaml"   
OUTPUT_DIR = "data_csv"   


os.makedirs(OUTPUT_DIR, exist_ok=True)

def yaml_to_csv():
    stock_data = {}

    for root, _, files in os.walk(INPUT_DIR):
        for file in files:
            if file.endswith(".yaml") or file.endswith(".yml"):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    data = yaml.safe_load(f)

                
                for date, entries in data.items():
                    for symbol, values in entries.items():
                        if symbol not in stock_data:
                            stock_data[symbol] = []
                        record = {
                            "Date": date,
                            "Open": values.get("open"),
                            "High": values.get("high"),
                            "Low": values.get("low"),
                            "Close": values.get("close"),
                            "Volume": values.get("volume")
                        }
                        stock_data[symbol].append(record)


    all_data = []
    for ticker, records in stock_data.items():
        df = pd.DataFrame(records)
        df["ticker"] = ticker  
        output_file = os.path.join(OUTPUT_DIR, f"{symbol}.csv")
        df.to_csv(output_file, index=False)
        print(f"Saved {output_file}")
        all_data.append(df)

    if all_data:
        master_df = pd.concat(all_data, ignore_index=True)
        master_file = os.path.join(OUTPUT_DIR, "master_csv.csv")
        master_df.to_csv(master_file, index=False)
        print(f"Saved {master_file}")

if __name__ == "__main__":
    yaml_to_csv()

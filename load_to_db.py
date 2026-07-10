import psycopg2

conn = psycopg2.connect(
    dbname="stock_analysis",
    user="postgres",
    password="123456789",
    host="localhost",
    port="5432"
)
print("✅ Connected successfully")
conn.close()

import pandas as pd
from sqlalchemy import create_engine
import streamlit as st


engine = create_engine("postgresql://postgres:123456789@localhost:5432/stock_analysis")

stock_df = pd.read_csv(r"C:\Users\Welcome\Desktop\stock_analys\data\master_csv.csv")
sector_df = pd.read_csv("sector.csv")


stock_df.to_sql("stock_data", engine, if_exists="replace", index=False)
sector_df.to_sql("sector_mapping", engine, if_exists="replace", index=False)

st.write("✅ Data loaded into SQL successfully")


query = """
WITH monthly_returns AS (
    SELECT 
        symbol,
        DATE_TRUNC('month', date) AS month,
        (MAX(close) - MIN(close)) / MIN(close) AS monthly_return
    FROM stock_data
    GROUP BY symbol, DATE_TRUNC('month', date)
)
SELECT *
FROM (
    SELECT symbol, month, monthly_return,
           ROW_NUMBER() OVER (PARTITION BY month ORDER BY monthly_return DESC) AS rank_gainer,
           ROW_NUMBER() OVER (PARTITION BY month ORDER BY monthly_return ASC) AS rank_loser
    FROM monthly_returns
) ranked
WHERE rank_gainer <= 5 OR rank_loser <= 5
ORDER BY month, monthly_return DESC;
"""

df = pd.read_sql(query, engine)
st.dataframe(df.head())

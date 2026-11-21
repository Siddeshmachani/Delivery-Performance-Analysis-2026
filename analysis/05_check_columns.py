import pandas as pd

df = pd.read_csv("analysis/cleaned_APL_Logistics.csv")

print("\n========== ALL DATASET COLUMNS ==========")

for column in df.columns:
    print(column)

print("\n========== DATE COLUMNS ==========")

for column in df.columns:
    if "date" in column.lower():
        print(column, df[column].dtype)

print("\n========== CUSTOMER SEGMENTS ==========")

print(df["Customer Segment"].value_counts())

print("\n========== MARKETS ==========")

print(df["Market"].value_counts())
import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv(
    "dataset/APL_Logistics.csv",
    encoding="latin1"
)

# Display dataset information
print("\n========== DATASET OVERVIEW ==========")

print("Total Rows:", df.shape[0])
print("Total Columns:", df.shape[1])

print("\n========== FIRST 5 ROWS ==========")

print(df.head())

print("\n========== COLUMN INFORMATION ==========")

print(df.info())

print("\n========== MISSING VALUES ==========")

print(df.isnull().sum())

print("\n========== DUPLICATE RECORDS ==========")

print(df.duplicated().sum())

print("\n========== DELIVERY STATUS ==========")

print(df["Delivery Status"].value_counts())

print("\n========== SHIPPING MODES ==========")

print(df["Shipping Mode"].value_counts())

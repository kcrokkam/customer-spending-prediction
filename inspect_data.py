
import pandas as pd

file_path = "data/raw/online_retail_II.xlsx"

df = pd.read_excel(
    file_path,
    sheet_name="Year 2010-2011"
)

print("Dataset shape:", df.shape)

print("\nDate range:")
print(df["InvoiceDate"].min())
print(df["InvoiceDate"].max())

print("\nUnique customers:")
print(df["Customer ID"].nunique())

print("\nUnique invoices:")
print(df["Invoice"].nunique())

print("\nMissing values:")
print(df.isna().sum())

print("\nNegative quantities:")
print((df["Quantity"] < 0).sum())

print("\nZero or negative prices:")
print((df["Price"] <= 0).sum())

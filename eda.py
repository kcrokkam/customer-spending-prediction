import pandas as pd
import matplotlib.pyplot as plt


# STEP 1: Load data
df = pd.read_excel(
    "data/raw/online_retail_II.xlsx",
    sheet_name="Year 2010-2011"
)


# STEP 2: Clean customer transactions
clean_df = df.dropna(subset=["Customer ID"]).copy()

clean_df = clean_df[
    (clean_df["Price"] > 0) &
    (clean_df["Quantity"] != 0)
].copy()

# Keep negative quantities to account for cancellations
clean_df["LineAmount"] = (
    clean_df["Quantity"] * clean_df["Price"]
)


# STEP 3: Data cleaning summary
print("\nCLEANING SUMMARY")
print("Original rows:", len(df))
print("Cleaned rows:", len(clean_df))
print("Unique customers:", clean_df["Customer ID"].nunique())

cancellations = (
    clean_df["Invoice"].astype(str).str.startswith("C").sum()
)
print("Remaining cancellation rows:", cancellations)

print("\nLINE AMOUNT SUMMARY")
print(clean_df["LineAmount"].describe())


# STEP 4: Examine extreme transactions
extreme = clean_df.loc[
    clean_df["LineAmount"].abs().nlargest(10).index
]

print("\nTOP 10 EXTREME TRANSACTIONS")
print(
    extreme[
        ["Invoice", "InvoiceDate", "Customer ID",
         "Quantity", "Price", "LineAmount"]
    ].to_string(index=False)
)


# STEP 5: Calculate customer-level net spending
customer_spending = (
    clean_df.groupby("Customer ID")["LineAmount"]
    .sum()
)

print("\nCUSTOMER SPENDING SUMMARY")
print(customer_spending.describe())

print("\nCustomers with negative net spending:")
print((customer_spending < 0).sum())


# STEP 6: Prepare spending distribution for visualization
# Exclude top 1% of positive spenders from the chart only
positive_spending = customer_spending[customer_spending > 0]

cutoff = positive_spending.quantile(0.99)

plot_data = customer_spending[
    customer_spending <= cutoff
]

print("\n99th percentile spending cutoff:", round(cutoff, 2))
print("Customers included in chart:", len(plot_data))


# STEP 7: Visualize customer spending distribution
plt.figure(figsize=(9, 5))

plt.hist(
    plot_data,
    bins=40,
    edgecolor="black"
)

plt.xlabel("Customer Net Spending (£)")
plt.ylabel("Number of Customers")
plt.title("Customer Net Spending Distribution (Top 1% Excluded)")

plt.tight_layout()

plt.savefig(
    "reports/figures/customer_spending.png",
    dpi=150
)

plt.close()

print("\nChart saved: reports/figures/customer_spending.png")
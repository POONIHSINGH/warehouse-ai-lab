import pandas as pd

required_columns = {
    "order_id",
    "sku",
    "zone",
    "quantity",
    "inventory_available",
    "pick_time_min",
    "fault_count",
    "downtime_min",
}


def load_orders(file_path):
    orders = pd.read_csv(file_path)

    missing_columns = required_columns - set(orders.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    return orders


df = load_orders("data/warehouse_orders.csv")

##print(df)

print(df.head())

df.info()
# Compare requested quantity with available inventory for each order.
downtime_threshold_min = 30
df["high_downtime"] = df["downtime_min"] > downtime_threshold_min

# Keep only orders where that comparison is True.
at_risk_orders = df.loc[
    df["high_downtime"],
    ["order_id", "sku", "zone", "quantity", "inventory_available","downtime_min"]
]
at_risk_orders = at_risk_orders.sort_values(
    by="downtime_min",
    ascending=False
)
print(f"\nOrders with downtime greater than {downtime_threshold_min} minutes:")
if at_risk_orders.empty:
    print(f"No orders exceeded {downtime_threshold_min} minutes of downtime.")
else:
    print(at_risk_orders.to_string(index=False))

print(f"\nOrders flagged: {len(at_risk_orders)} of {len(df)}")
high_downtime_pct = len(at_risk_orders) / len(df) * 100
print(f"\nPercentage of orders flagged: {high_downtime_pct:.2f}%")
#calculate total downtime by zone
zone_downtime = df.groupby("zone")["downtime_min"].sum()
#print total downtime by zone in new line
zone_downtime = zone_downtime.sort_values(ascending=False)
print("\nTotal downtime by zone:")
print(zone_downtime)
#average downtime by zone
zone_average_downtime = df.groupby("zone")["downtime_min"].mean()
zone_average_downtime = zone_average_downtime.sort_values(ascending=False)
print("\nAverage downtime by zone:")
print(zone_average_downtime.round(2))
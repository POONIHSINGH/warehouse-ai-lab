import pandas as pd

inventory = pd.read_csv("data/crane_impact_sample.csv")
outbound = pd.read_csv("data/outbound_orders_sample.csv")

sku = "SKU-A"
available = int(
    inventory.loc[inventory["sku"] == sku, "dms_available_qty"].iloc[0]
)

sku_orders = outbound.loc[outbound["sku"] == sku].sort_values(
    ["ship_by", "order_id"]
)

for order in sku_orders.itertuples(index=False):
    allocated = min(order.order_qty, available)

    # Write these two lines yourself:
    at_risk = order.order_qty - allocated
    available = available - allocated

    print(order.order_id, "allocated:", allocated, "at risk:", at_risk)
import json
import pandas as pd


def orders_at_risk(failed_crane_id, inventory, outbound):
    """Return outbound orders that can't be fully filled while a crane is down."""
    crane_skus = inventory.loc[inventory["crane_id"] == failed_crane_id]
    if crane_skus.empty:
        raise ValueError(f"No inventory rows found for {failed_crane_id}.")

    results = []
    for item in crane_skus.itertuples(index=False):
        available = int(item.dms_available_qty)
        sku_orders = outbound.loc[outbound["sku"] == item.sku].sort_values(
            ["ship_by", "order_id"]
        )
        for order in sku_orders.itertuples(index=False):
            allocated = min(int(order.order_qty), available)
            at_risk = int(order.order_qty) - allocated
            available = available - allocated

            if at_risk > 0:
                results.append({
                    "order_id": order.order_id,
                    "sku": order.sku,
                    "ship_by": order.ship_by,
                    "order_qty": int(order.order_qty),
                    "allocated": allocated,
                    "at_risk_qty": at_risk,
                })
    return results


if __name__ == "__main__":
    inventory = pd.read_csv("data/crane_impact_sample.csv")
    outbound = pd.read_csv("data/outbound_orders_sample.csv")
    report = orders_at_risk("CRANE-01", inventory, outbound)
    print(json.dumps(report, indent=2))
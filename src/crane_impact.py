import json
import pandas as pd

orders = pd.read_csv("data/crane_impact_sample.csv")

orders["gap_units"] = (
    orders["forecast_night_qty"] - orders["dms_available_qty"]
).clip(lower=0)

#print(orders[["sku", "dms_available_qty", "forecast_night_qty", "gap_units"]])

failed_crane_id = "CRANE-01"
#write a check to see if any rows exist for the failed crane id, if not raise a ValueError with the message "No inventory rows found for {failed_crane_id}. Check the crane ID or data feed."
if not (orders["crane_id"] == failed_crane_id).any():
    raise ValueError(f"No inventory rows found for {failed_crane_id}. Check the crane ID or data feed.")
at_risk = orders.loc[
    (orders["crane_id"] == failed_crane_id) & (orders["gap_units"] > 0),
    ["sku", "dms_available_qty", "forecast_night_qty", "gap_units"],
]

#print(f"\nPotential DMS gaps while {failed_crane_id} is unavailable:")
#print(at_risk.to_string(index=False))

report = {
    "failed_crane_id": failed_crane_id,
    "potential_gaps": at_risk.to_dict(orient="records"),
}

print(json.dumps(report, indent=2))
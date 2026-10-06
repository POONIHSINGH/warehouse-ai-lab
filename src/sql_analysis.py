import sqlite3

import pandas as pd

csv_path = "data/warehouse_orders.csv"
database_path = "data/warehouse_operations.db"

orders = pd.read_csv(csv_path)

connection = sqlite3.connect(database_path)

orders.to_sql(
    "orders",
    connection,
    if_exists="replace",
    index=False,
)

print(f"Loaded {len(orders)} rows into the orders table.")
query = """
WITH zones AS (
    SELECT DISTINCT zone FROM orders
),
thresholds(limit_min) AS (
    VALUES (20), (30)
)
SELECT zones.zone, thresholds.limit_min
FROM zones
CROSS JOIN thresholds
ORDER BY zones.zone, thresholds.limit_min
"""

high_downtime_orders = pd.read_sql_query(
    query,
    connection
)

print("\nOrders with downtime greater than 20 minutes:")
print(high_downtime_orders.to_string(index=False))
connection.close()
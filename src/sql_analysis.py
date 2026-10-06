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

SELECT
    zone,
    COUNT(*)                     AS orders,
    SUM(downtime_min)           AS total_downtime_min,
    ROUND(AVG(downtime_min), 2) AS avg_downtime_min
FROM orders
GROUP BY zone
ORDER BY total_downtime_min DESC
"""

zone_downtimes = pd.read_sql_query(
    query,
    connection
)

print("\nDowntime by zone (worst first):")
print(zone_downtimes.to_string(index=False))
connection.close()
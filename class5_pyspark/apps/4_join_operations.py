"""
Join Operations Example
Combining multiple DataFrames
"""
from pyspark.sql import SparkSession

# Create Spark Session
spark = SparkSession.builder \
    .appName("JoinOperations") \
    .master("local[*]") \
    .getOrCreate()

# Sample data - Customers
customers = [
    (1, "John Doe", "New York"),
    (2, "Jane Smith", "Los Angeles"),
    (3, "Bob Johnson", "Chicago"),
    (4, "Alice Brown", "Houston")
]
customer_df = spark.createDataFrame(customers, ["customer_id", "name", "city"])

# Sample data - Orders
orders = [
    (101, 1, 250.00),
    (102, 2, 150.00),
    (103, 1, 300.00),
    (104, 3, 200.00),
    (105, 2, 450.00),
    (106, 5, 100.00)  # customer_id 5 doesn't exist in customers
]
order_df = spark.createDataFrame(orders, ["order_id", "customer_id", "amount"])

print("\n=== Customers ===")
customer_df.show()

print("\n=== Orders ===")
order_df.show()

# Inner Join - only matching records
print("\n=== Inner Join: Customers with Orders ===")
inner_join = customer_df.join(order_df, "customer_id", "inner")
inner_join.show()

# Left Join - all customers, with or without orders
print("\n=== Left Join: All Customers ===")
left_join = customer_df.join(order_df, "customer_id", "left")
left_join.show()

# Aggregate: Total amount per customer
print("\n=== Total Order Amount per Customer ===")
customer_totals = customer_df.join(order_df, "customer_id", "left") \
    .groupBy("customer_id", "name", "city") \
    .agg({"amount": "sum"}) \
    .withColumnRenamed("sum(amount)", "total_amount") \
    .orderBy("customer_id")
customer_totals.show()

spark.stop()

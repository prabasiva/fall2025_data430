"""
Data Aggregation Example
Statistical operations and aggregations
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, max, min, sum, count

# Create Spark Session
spark = SparkSession.builder \
    .appName("DataAggregation") \
    .master("local[*]") \
    .getOrCreate()

# Sample data - Product sales
sales_data = [
    ("Laptop", "Electronics", 1200, 5),
    ("Mouse", "Electronics", 25, 50),
    ("Desk", "Furniture", 300, 10),
    ("Chair", "Furniture", 150, 20),
    ("Keyboard", "Electronics", 75, 30),
    ("Monitor", "Electronics", 400, 15),
    ("Table", "Furniture", 250, 8)
]

columns = ["product", "category", "price", "quantity"]
df = spark.createDataFrame(sales_data, columns)

print("\n=== Sales Data ===")
df.show()

# Calculate total revenue
df_with_revenue = df.withColumn("revenue", col("price") * col("quantity"))

print("\n=== Sales with Revenue ===")
df_with_revenue.show()

# Aggregate statistics by category
print("\n=== Category Statistics ===")
category_stats = df_with_revenue.groupBy("category").agg(
    count("product").alias("num_products"),
    sum("revenue").alias("total_revenue"),
    avg("price").alias("avg_price"),
    max("quantity").alias("max_quantity"),
    min("quantity").alias("min_quantity")
)
category_stats.show()

# Overall statistics
print("\n=== Overall Statistics ===")
overall_stats = df_with_revenue.agg(
    sum("revenue").alias("total_revenue"),
    avg("price").alias("avg_price"),
    count("product").alias("total_products")
)
overall_stats.show()

spark.stop()

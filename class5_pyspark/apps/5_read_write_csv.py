"""
Reading and Writing CSV Files
File I/O operations with PySpark
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, month

# Create Spark Session
spark = SparkSession.builder \
    .appName("ReadWriteCSV") \
    .master("local[*]") \
    .getOrCreate()

# Create sample data
sample_data = [
    ("2024-01-15", "Product A", 100, 50),
    ("2024-01-20", "Product B", 150, 30),
    ("2024-02-10", "Product A", 120, 45),
    ("2024-02-15", "Product C", 200, 25),
    ("2024-03-05", "Product B", 180, 35),
    ("2024-03-20", "Product A", 110, 55)
]

columns = ["date", "product", "price", "quantity"]
df = spark.createDataFrame(sample_data, columns)

print("\n=== Original Data ===")
df.show()

# Write to CSV
output_path = "/data/sales_data.csv"
print(f"\n=== Writing to {output_path} ===")
df.write.mode("overwrite").option("header", "true").csv(output_path)
print("Data written successfully!")

# Read from CSV
print(f"\n=== Reading from {output_path} ===")
df_read = spark.read.option("header", "true").option("inferSchema", "true").csv(output_path)
df_read.show()

# Transform and write processed data
print("\n=== Processing and Writing Summary ===")
df_read_typed = df_read.withColumn("price", col("price").cast("int")) \
    .withColumn("quantity", col("quantity").cast("int"))

summary = df_read_typed.groupBy("product").agg(
    {"price": "avg", "quantity": "sum"}
).withColumnRenamed("avg(price)", "avg_price") \
 .withColumnRenamed("sum(quantity)", "total_quantity")

summary.show()

# Write summary
summary_path = "/data/sales_summary.csv"
summary.write.mode("overwrite").option("header", "true").csv(summary_path)
print(f"Summary written to {summary_path}")

# Show what files were created
print("\n=== Files Created ===")
print("1. /data/sales_data.csv/")
print("2. /data/sales_summary.csv/")

spark.stop()

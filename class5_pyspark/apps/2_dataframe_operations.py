"""
DataFrame Operations Example
Filter, select, and transform data
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, upper

# Create Spark Session
spark = SparkSession.builder \
    .appName("DataFrameOperations") \
    .master("local[*]") \
    .getOrCreate()

# Sample data - Employee records
data = [
    ("John", "Sales", 5000, 28),
    ("Alice", "Engineering", 8000, 32),
    ("Bob", "Sales", 6000, 35),
    ("Charlie", "Engineering", 9000, 29),
    ("Diana", "HR", 5500, 30),
    ("Eve", "Engineering", 7500, 27)
]

columns = ["name", "department", "salary", "age"]
df = spark.createDataFrame(data, columns)

print("\n=== Original DataFrame ===")
df.show()

# Filter employees with salary > 6000
print("\n=== High Earners (Salary > 6000) ===")
df.filter(col("salary") > 6000).show()

# Select specific columns with transformation
print("\n=== Names and Departments (Uppercase) ===")
df.select(upper(col("name")).alias("name"), col("department")).show()

# Group by department and calculate average salary
print("\n=== Average Salary by Department ===")
df.groupBy("department").avg("salary").show()

spark.stop()

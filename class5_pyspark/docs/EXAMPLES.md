# PySpark Examples and Tutorials

Comprehensive collection of PySpark examples for learning and reference.

## Table of Contents

1. [Basic DataFrame Operations](#basic-dataframe-operations)
2. [Data Loading and Saving](#data-loading-and-saving)
3. [Transformations](#transformations)
4. [Aggregations](#aggregations)
5. [Joins](#joins)
6. [Window Functions](#window-functions)
7. [Working with Dates](#working-with-dates)
8. [String Operations](#string-operations)
9. [Machine Learning Basics](#machine-learning-basics)
10. [Performance Optimization](#performance-optimization)

---

## Basic DataFrame Operations

### Creating DataFrames

```python
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# Initialize Spark
spark = SparkSession.builder \
    .appName("Examples") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# Method 1: From lists
data = [("Alice", 34), ("Bob", 45), ("Charlie", 28)]
df = spark.createDataFrame(data, ["name", "age"])
df.show()

# Method 2: With explicit schema
schema = StructType([
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True)
])
df = spark.createDataFrame(data, schema)
df.show()

# Method 3: From dictionaries
data = [
    {"name": "Alice", "age": 34, "city": "NYC"},
    {"name": "Bob", "age": 45, "city": "LA"},
    {"name": "Charlie", "age": 28, "city": "Chicago"}
]
df = spark.createDataFrame(data)
df.show()
```

### Inspecting DataFrames

```python
# Show first n rows
df.show(5)
df.show(5, truncate=False)  # Don't truncate long strings

# Get schema
df.printSchema()

# Get column names
print(df.columns)

# Count rows
print(f"Total rows: {df.count()}")

# Get statistics
df.describe().show()

# Sample rows
df.sample(fraction=0.5).show()

# First row
print(df.first())

# Take n rows as list
rows = df.take(3)
for row in rows:
    print(row)
```

### Selecting Columns

```python
from pyspark.sql.functions import col

# Select specific columns
df.select("name", "age").show()

# Using col()
df.select(col("name"), col("age")).show()

# With aliases
df.select(col("name").alias("employee_name")).show()

# Select all columns
df.select("*").show()

# Drop columns
df.drop("age").show()
```

### Filtering Rows

```python
from pyspark.sql.functions import col

# Simple filter
df.filter(col("age") > 30).show()

# Multiple conditions (AND)
df.filter((col("age") > 30) & (col("city") == "NYC")).show()

# Multiple conditions (OR)
df.filter((col("age") > 40) | (col("city") == "Chicago")).show()

# Using SQL-like syntax
df.filter("age > 30").show()

# NOT condition
df.filter(~(col("age") > 30)).show()

# IN clause
df.filter(col("city").isin(["NYC", "LA"])).show()

# LIKE operator
df.filter(col("name").like("%li%")).show()

# IS NULL / IS NOT NULL
df.filter(col("age").isNull()).show()
df.filter(col("age").isNotNull()).show()
```

---

## Data Loading and Saving

### CSV Files

```python
# Read CSV
df = spark.read.csv("/data/input.csv", header=True, inferSchema=True)

# Read with options
df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .option("delimiter", ",") \
    .option("quote", '"') \
    .csv("/data/input.csv")

# Write CSV
df.write.mode("overwrite").csv("/data/output.csv", header=True)

# Write with options
df.write \
    .mode("overwrite") \
    .option("header", "true") \
    .option("delimiter", "|") \
    .csv("/data/output.csv")
```

### JSON Files

```python
# Read JSON
df = spark.read.json("/data/input.json")

# Read multiline JSON
df = spark.read.option("multiline", "true").json("/data/input.json")

# Write JSON
df.write.mode("overwrite").json("/data/output.json")

# Pretty print
df.write.mode("overwrite") \
    .option("compression", "none") \
    .json("/data/output.json")
```

### Parquet Files (Recommended)

```python
# Read Parquet (columnar format, very efficient)
df = spark.read.parquet("/data/input.parquet")

# Write Parquet
df.write.mode("overwrite").parquet("/data/output.parquet")

# With compression
df.write.mode("overwrite") \
    .option("compression", "snappy") \
    .parquet("/data/output.parquet")

# Partitioned by column
df.write.mode("overwrite") \
    .partitionBy("city") \
    .parquet("/data/output.parquet")
```

### Multiple Files

```python
# Read all CSVs in directory
df = spark.read.csv("/data/csv_files/*.csv", header=True)

# Read specific pattern
df = spark.read.csv("/data/sales_2024_*.csv", header=True)

# Read from multiple paths
df = spark.read.csv(["/data/file1.csv", "/data/file2.csv"], header=True)
```

---

## Transformations

### Adding Columns

```python
from pyspark.sql.functions import col, lit, when, concat

# Add constant column
df = df.withColumn("country", lit("USA"))

# Add calculated column
df = df.withColumn("age_next_year", col("age") + 1)

# Conditional column
df = df.withColumn("age_group",
    when(col("age") < 30, "Young")
    .when(col("age") < 50, "Middle")
    .otherwise("Senior")
)

# Multiple conditions
df = df.withColumn("status",
    when((col("age") > 30) & (col("city") == "NYC"), "NYC Senior")
    .when((col("age") > 30) & (col("city") == "LA"), "LA Senior")
    .otherwise("Other")
)

# Concatenate strings
df = df.withColumn("full_info", concat(col("name"), lit(" - "), col("city")))
```

### Renaming Columns

```python
# Rename one column
df = df.withColumnRenamed("name", "employee_name")

# Rename multiple columns
df = df.toDF("emp_name", "emp_age", "emp_city")

# Using select with alias
df = df.select(
    col("name").alias("employee_name"),
    col("age").alias("employee_age")
)
```

### Dropping Duplicates

```python
# Drop all duplicates
df = df.dropDuplicates()

# Drop duplicates based on specific columns
df = df.dropDuplicates(["name", "city"])

# Alias
df = df.distinct()
```

### Handling NULL Values

```python
# Drop rows with any NULL
df = df.dropna()

# Drop rows where all values are NULL
df = df.dropna(how="all")

# Drop rows with NULL in specific columns
df = df.dropna(subset=["name", "age"])

# Fill NULL with default values
df = df.fillna(0)  # All nulls become 0
df = df.fillna({"age": 0, "city": "Unknown"})  # Different defaults per column

# Replace specific values
df = df.replace("", "Unknown", subset=["city"])
```

### Sorting

```python
from pyspark.sql.functions import col, desc, asc

# Sort ascending
df = df.orderBy("age")
df = df.sort("age")  # Same as orderBy

# Sort descending
df = df.orderBy(col("age").desc())

# Multiple columns
df = df.orderBy(col("city").asc(), col("age").desc())

# Sort with nulls
df = df.orderBy(col("age").asc_nulls_first())
df = df.orderBy(col("age").desc_nulls_last())
```

---

## Aggregations

### Basic Aggregations

```python
from pyspark.sql.functions import count, sum, avg, max, min, stddev

# Count
df.select(count("*")).show()

# Multiple aggregations
df.select(
    count("*").alias("total"),
    avg("age").alias("avg_age"),
    max("age").alias("max_age"),
    min("age").alias("min_age")
).show()

# GroupBy
df.groupBy("city") \
    .agg(
        count("*").alias("count"),
        avg("age").alias("avg_age")
    ).show()

# Multiple group by columns
df.groupBy("city", "age_group") \
    .agg(count("*").alias("count")) \
    .show()
```

### Advanced Aggregations

```python
from pyspark.sql.functions import (
    countDistinct, collect_list, collect_set,
    first, last, approx_count_distinct
)

df.groupBy("city").agg(
    count("*").alias("total"),
    countDistinct("name").alias("unique_names"),
    collect_list("name").alias("all_names"),
    collect_set("name").alias("unique_name_list"),
    first("name").alias("first_name"),
    last("name").alias("last_name")
).show(truncate=False)

# Approximate distinct count (faster for large datasets)
df.select(approx_count_distinct("name", rsd=0.05)).show()
```

### Pivot Tables

```python
# Create pivot table
pivot_df = df.groupBy("city") \
    .pivot("age_group") \
    .agg(count("*"))

pivot_df.show()

# With specific values
pivot_df = df.groupBy("city") \
    .pivot("age_group", ["Young", "Middle", "Senior"]) \
    .agg(count("*"))

pivot_df.show()
```

---

## Joins

### Join Types

```python
# Create sample dataframes
employees = spark.createDataFrame([
    (1, "Alice", 100),
    (2, "Bob", 200),
    (3, "Charlie", 100)
], ["emp_id", "name", "dept_id"])

departments = spark.createDataFrame([
    (100, "Engineering"),
    (200, "Sales"),
    (300, "Marketing")
], ["dept_id", "dept_name"])

# Inner join (default)
result = employees.join(departments, "dept_id", "inner")
result.show()

# Left outer join
result = employees.join(departments, "dept_id", "left")
result.show()

# Right outer join
result = employees.join(departments, "dept_id", "right")
result.show()

# Full outer join
result = employees.join(departments, "dept_id", "outer")
result.show()

# Left semi join (like IN clause)
result = employees.join(departments, "dept_id", "left_semi")
result.show()

# Left anti join (like NOT IN)
result = employees.join(departments, "dept_id", "left_anti")
result.show()
```

### Join Conditions

```python
# Join on multiple columns
result = df1.join(df2, ["col1", "col2"], "inner")

# Join with different column names
result = df1.join(df2, df1.id == df2.emp_id, "inner")

# Complex join conditions
result = df1.join(
    df2,
    (df1.id == df2.emp_id) & (df1.dept == df2.dept),
    "inner"
)

# Select specific columns after join
result = df1.alias("e").join(
    df2.alias("d"),
    col("e.dept_id") == col("d.dept_id"),
    "inner"
).select("e.name", "d.dept_name")
```

### Broadcast Joins (for small tables)

```python
from pyspark.sql.functions import broadcast

# Broadcast small table for faster joins
result = large_df.join(broadcast(small_df), "key")
```

---

## Window Functions

### Ranking

```python
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, rank, dense_rank

# Create sample data
sales = spark.createDataFrame([
    ("Alice", "2024-01", 1000),
    ("Alice", "2024-02", 1500),
    ("Bob", "2024-01", 800),
    ("Bob", "2024-02", 1200),
    ("Charlie", "2024-01", 2000),
    ("Charlie", "2024-02", 1800)
], ["name", "month", "sales"])

# Define window
window_spec = Window.partitionBy("name").orderBy(col("sales").desc())

# Add rankings
result = sales.withColumn("row_num", row_number().over(window_spec)) \
    .withColumn("rank", rank().over(window_spec)) \
    .withColumn("dense_rank", dense_rank().over(window_spec))

result.show()
```

### Running Totals and Moving Averages

```python
from pyspark.sql.functions import sum, avg, lag, lead

# Window for cumulative sum
window_spec = Window.partitionBy("name").orderBy("month") \
    .rowsBetween(Window.unboundedPreceding, Window.currentRow)

result = sales.withColumn("cumulative_sales", sum("sales").over(window_spec))
result.show()

# Moving average (last 2 months)
window_spec = Window.partitionBy("name").orderBy("month") \
    .rowsBetween(-1, 0)  # Current and previous row

result = sales.withColumn("moving_avg", avg("sales").over(window_spec))
result.show()

# Lag and Lead
window_spec = Window.partitionBy("name").orderBy("month")

result = sales \
    .withColumn("prev_sales", lag("sales", 1).over(window_spec)) \
    .withColumn("next_sales", lead("sales", 1).over(window_spec)) \
    .withColumn("sales_change", col("sales") - lag("sales", 1).over(window_spec))

result.show()
```

---

## Working with Dates

```python
from pyspark.sql.functions import (
    current_date, current_timestamp, to_date, to_timestamp,
    year, month, dayofmonth, dayofweek, hour, minute,
    date_add, date_sub, datediff, months_between,
    date_format, unix_timestamp, from_unixtime
)

# Create sample data with dates
df = spark.createDataFrame([
    ("2024-01-15",),
    ("2024-02-20",),
    ("2024-03-10",)
], ["date_string"])

# Convert string to date
df = df.withColumn("date", to_date(col("date_string"), "yyyy-MM-dd"))

# Extract date parts
df = df \
    .withColumn("year", year("date")) \
    .withColumn("month", month("date")) \
    .withColumn("day", dayofmonth("date")) \
    .withColumn("day_of_week", dayofweek("date"))

df.show()

# Date arithmetic
df = df \
    .withColumn("date_plus_7", date_add("date", 7)) \
    .withColumn("date_minus_7", date_sub("date", 7))

df.show()

# Current date/time
df = df \
    .withColumn("today", current_date()) \
    .withColumn("now", current_timestamp())

# Date difference
df = df.withColumn("days_from_today", datediff(current_date(), col("date")))

# Format date
df = df.withColumn("formatted", date_format("date", "MMM dd, yyyy"))

df.show(truncate=False)
```

---

## String Operations

```python
from pyspark.sql.functions import (
    upper, lower, trim, ltrim, rtrim,
    concat, concat_ws, substring, length,
    regexp_replace, regexp_extract, split,
    initcap, reverse
)

# Create sample data
df = spark.createDataFrame([
    ("  Hello World  ",),
    ("APACHE SPARK",),
    ("pyspark-tutorial",)
], ["text"])

# Case conversion
df = df \
    .withColumn("upper", upper("text")) \
    .withColumn("lower", lower("text")) \
    .withColumn("initcap", initcap("text"))

df.show(truncate=False)

# Trimming
df = df \
    .withColumn("trimmed", trim("text")) \
    .withColumn("ltrimmed", ltrim("text")) \
    .withColumn("rtrimmed", rtrim("text"))

# String operations
df = df \
    .withColumn("length", length("text")) \
    .withColumn("substring", substring("text", 1, 5)) \
    .withColumn("reversed", reverse("text"))

# Replace patterns
df = spark.createDataFrame([("Phone: 123-456-7890",)], ["text"])

df = df.withColumn(
    "numbers_only",
    regexp_replace("text", "[^0-9]", "")
)

df.show(truncate=False)

# Extract patterns
df = df.withColumn(
    "area_code",
    regexp_extract("text", r"(\d{3})-\d{3}-\d{4}", 1)
)

# Split strings
df = spark.createDataFrame([("a,b,c",)], ["text"])
df = df.withColumn("array", split("text", ","))
df.show(truncate=False)
```

---

## Machine Learning Basics

### Linear Regression Example

```python
from pyspark.ml.regression import LinearRegression
from pyspark.ml.feature import VectorAssembler

# Create sample data
data = spark.createDataFrame([
    (1.0, 2.0, 3.0),
    (2.0, 3.0, 5.0),
    (3.0, 4.0, 7.0),
    (4.0, 5.0, 9.0)
], ["feature1", "feature2", "label"])

# Assemble features
assembler = VectorAssembler(
    inputCols=["feature1", "feature2"],
    outputCol="features"
)

df = assembler.transform(data)

# Split data
train, test = df.randomSplit([0.8, 0.2], seed=42)

# Train model
lr = LinearRegression(labelCol="label", featuresCol="features")
model = lr.fit(train)

# Make predictions
predictions = model.transform(test)
predictions.select("features", "label", "prediction").show()

# Model summary
print(f"Coefficients: {model.coefficients}")
print(f"Intercept: {model.intercept}")
print(f"RMSE: {model.summary.rootMeanSquaredError}")
```

---

## Performance Optimization

### Caching

```python
# Cache DataFrame in memory
df.cache()
df.persist()

# Use the cached DataFrame
df.count()  # First action: computes and caches
df.filter(...).count()  # Second action: uses cache

# Unpersist when done
df.unpersist()
```

### Repartitioning

```python
# Check current partitions
print(f"Partitions: {df.rdd.getNumPartitions()}")

# Increase partitions (for parallelism)
df = df.repartition(10)

# Decrease partitions (for writing)
df = df.coalesce(1)

# Repartition by column (for joins)
df = df.repartition("city")
```

### Query Optimization

```python
# View execution plan
df.explain(True)

# Use broadcast for small tables
from pyspark.sql.functions import broadcast
result = large_df.join(broadcast(small_df), "key")

# Filter early
df = df.filter(col("important") == True)  # Do this first
df = df.select("col1", "col2")  # Then select

# Use column pruning
df.select("col1", "col2")  # Only needed columns
```

---

## Complete Example: Data Analysis Pipeline

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# Initialize
spark = SparkSession.builder \
    .appName("CompleteExample") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# 1. Load data
sales = spark.read.csv("/data/sales.csv", header=True, inferSchema=True)

# 2. Clean data
sales_clean = sales \
    .dropna(subset=["customer_id", "amount"]) \
    .withColumn("amount", col("amount").cast("double")) \
    .withColumn("date", to_date(col("date_string"), "yyyy-MM-dd")) \
    .filter(col("amount") > 0)

# 3. Add features
sales_enriched = sales_clean \
    .withColumn("year", year("date")) \
    .withColumn("month", month("date")) \
    .withColumn("quarter", quarter("date")) \
    .withColumn("revenue_category",
        when(col("amount") > 1000, "High")
        .when(col("amount") > 500, "Medium")
        .otherwise("Low")
    )

# 4. Aggregate
monthly_summary = sales_enriched \
    .groupBy("year", "month") \
    .agg(
        count("*").alias("num_transactions"),
        sum("amount").alias("total_revenue"),
        avg("amount").alias("avg_transaction"),
        countDistinct("customer_id").alias("unique_customers")
    ) \
    .orderBy("year", "month")

# 5. Save results
monthly_summary.write \
    .mode("overwrite") \
    .partitionBy("year") \
    .parquet("/data/monthly_summary.parquet")

# 6. Show sample
monthly_summary.show()

# Cleanup
spark.stop()
```

---

This covers the most common PySpark operations. For more advanced topics, refer to the [official PySpark documentation](https://spark.apache.org/docs/latest/api/python/).

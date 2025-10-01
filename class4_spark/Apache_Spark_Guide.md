# Apache Spark Comprehensive Guide

## Table of Contents
1. [What is Apache Spark](#what-is-apache-spark)
2. [Spark Architecture](#spark-architecture)
3. [Core Concepts](#core-concepts)
4. [Installation Guide](#installation-guide)
5. [PySpark Examples](#pyspark-examples)

## What is Apache Spark

Apache Spark is a unified analytics engine for large-scale data processing. It provides high-level APIs in Java, Scala, Python, and R, and an optimized engine that supports general execution graphs. It also supports a rich set of higher-level tools including Spark SQL for SQL and structured data processing, MLlib for machine learning, GraphX for graph processing, and Structured Streaming for incremental computation and stream processing.

### Key Features

- **Speed**: Spark runs workloads up to 100x faster than Hadoop MapReduce in memory, or 10x faster on disk
- **Ease of Use**: Simple APIs in Java, Scala, Python, R, and SQL
- **Generality**: Combines SQL, streaming, and complex analytics
- **Runs Everywhere**: Spark runs on Hadoop, Apache Mesos, Kubernetes, standalone, or in the cloud

### Use Cases

- **Batch Processing**: Large-scale data processing jobs
- **Stream Processing**: Real-time data processing
- **Machine Learning**: Distributed machine learning algorithms
- **Graph Processing**: Analysis of graph-structured data
- **Interactive Analytics**: Ad-hoc queries and exploration

## Spark Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Driver Program                       │
│  ┌─────────────────┐  ┌─────────────────────────────────┐│
│  │   SparkContext  │  │        SparkSession            ││
│  └─────────────────┘  └─────────────────────────────────┘│
└─────────────────────────────────────────────────────────┘
                            │
                            │ (Cluster Manager)
                            │
┌───────────────────────────────────────────────────────────┐
│                    Cluster Manager                       │
│         (Standalone, YARN, Mesos, Kubernetes)            │
└───────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼─────┐    ┌────────▼─────┐    ┌────────▼─────┐
│   Worker    │    │   Worker     │    │   Worker     │
│   Node 1    │    │   Node 2     │    │   Node 3     │
│             │    │              │    │              │
│ ┌─────────┐ │    │ ┌──────────┐ │    │ ┌──────────┐ │
│ │Executor │ │    │ │ Executor │ │    │ │ Executor │ │
│ │  Cache  │ │    │ │  Cache   │ │    │ │  Cache   │ │
│ │ Tasks   │ │    │ │  Tasks   │ │    │ │  Tasks   │ │
│ └─────────┘ │    │ └──────────┘ │    │ └──────────┘ │
└─────────────┘    └──────────────┘    └──────────────┘
```

### Components

#### 1. Driver Program
- Contains the main function and defines distributed datasets
- Creates SparkContext/SparkSession
- Converts user program into tasks
- Schedules tasks on executors

#### 2. Cluster Manager
- **Standalone**: Simple cluster manager included with Spark
- **YARN**: Hadoop's cluster manager
- **Mesos**: General cluster manager
- **Kubernetes**: Container orchestration platform

#### 3. Worker Nodes
- Run executor processes
- Store data in memory or disk storage
- Execute tasks

#### 4. Executors
- Run on worker nodes
- Execute tasks assigned by the driver
- Store data for the application in memory or disk storage

## Core Concepts

### 1. Resilient Distributed Datasets (RDDs)

RDDs are the fundamental data structure of Spark. They are:
- **Resilient**: Fault-tolerant through lineage
- **Distributed**: Partitioned across cluster nodes
- **Datasets**: Collections of data

#### RDD Characteristics
- **Immutable**: Cannot be changed after creation
- **Lazy Evaluation**: Transformations are not executed until an action is called
- **Partitioned**: Data is split across multiple nodes
- **Cacheable**: Can be stored in memory for faster access

#### RDD Operations

**Transformations** (Lazy):
- `map()`: Apply function to each element
- `filter()`: Filter elements based on condition
- `flatMap()`: Flatten and map
- `union()`: Combine two RDDs
- `join()`: Join two RDDs by key

**Actions** (Eager):
- `collect()`: Return all elements to driver
- `count()`: Count number of elements
- `first()`: Return first element
- `take(n)`: Return first n elements
- `reduce()`: Aggregate elements

### 2. DataFrames

DataFrames are distributed collections of data organized into named columns. They provide:
- **Schema**: Structured data with known column types
- **Optimization**: Catalyst optimizer for query optimization
- **APIs**: SQL-like operations

### 3. Datasets

Datasets combine the benefits of RDDs and DataFrames:
- **Type Safety**: Compile-time type checking
- **Performance**: Catalyst optimizer
- **Object-Oriented**: Work with domain objects

### 4. Spark SQL

Spark SQL provides:
- SQL queries on structured data
- Integration with DataFrames and Datasets
- Connectivity to various data sources

### 5. Streaming

Spark Streaming enables:
- Real-time data processing
- Micro-batch processing
- Integration with various streaming sources

## Installation Guide

### Prerequisites

- Java 8 or later
- Python 3.6+ (for PySpark)
- Scala 2.12 (optional, for Scala development)

### Method 1: Standalone Installation

#### Step 1: Download Spark
```bash
# Download Spark (replace with latest version)
curl -O https://archive.apache.org/dist/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz

# Extract
tar -xzf spark-3.5.0-bin-hadoop3.tgz

# Move to desired location
sudo mv spark-3.5.0-bin-hadoop3 /opt/spark
```

#### Step 2: Set Environment Variables
```bash
# Add to ~/.bashrc or ~/.zshrc
export SPARK_HOME=/opt/spark
export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
export PYSPARK_PYTHON=python3
```

#### Step 3: Verify Installation
```bash
# Start Spark shell
spark-shell

# Start PySpark
pyspark

# Check version
spark-submit --version
```

### Method 2: Using Package Managers

#### Using Homebrew (macOS)
```bash
brew install apache-spark
```

#### Using pip (PySpark only)
```bash
pip install pyspark
```

#### Using conda
```bash
conda install pyspark
```

### Method 3: Docker Installation

#### Pull Spark Docker Image
```bash
docker pull apache/spark:latest
```

#### Run Spark Container
```bash
# Run PySpark
docker run -it apache/spark:latest /opt/spark/bin/pyspark

# Run with volume mount
docker run -it -v $(pwd):/workspace apache/spark:latest /opt/spark/bin/pyspark
```

### Configuration

#### Spark Configuration Files
- `spark-defaults.conf`: Default configuration properties
- `spark-env.sh`: Environment variables
- `log4j.properties`: Logging configuration

#### Example spark-defaults.conf
```properties
spark.master                     local[*]
spark.sql.warehouse.dir          /tmp/spark-warehouse
spark.sql.adaptive.enabled       true
spark.sql.adaptive.coalescePartitions.enabled true
spark.executor.memory            2g
spark.driver.memory              1g
```

## PySpark Examples

### Setting Up PySpark

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Create SparkSession
spark = SparkSession.builder \
    .appName("SparkExample") \
    .config("spark.sql.adaptive.enabled", "true") \
    .getOrCreate()

# Set log level
spark.sparkContext.setLogLevel("WARN")
```

### Example 1: Basic RDD Operations

```python
# Create RDD from list
numbers = spark.sparkContext.parallelize([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Transformations
even_numbers = numbers.filter(lambda x: x % 2 == 0)
squared_numbers = numbers.map(lambda x: x ** 2)

# Actions
print("Even numbers:", even_numbers.collect())
print("Sum of squares:", squared_numbers.reduce(lambda a, b: a + b))
print("Count:", numbers.count())
```

### Example 2: Working with DataFrames

```python
# Create DataFrame from data
data = [
    ("Alice", 25, "Engineer"),
    ("Bob", 30, "Manager"),
    ("Charlie", 35, "Engineer"),
    ("David", 28, "Analyst"),
    ("Eve", 32, "Manager")
]

schema = StructType([
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True),
    StructField("job", StringType(), True)
])

df = spark.createDataFrame(data, schema)

# Show DataFrame
df.show()

# Basic operations
print("Schema:")
df.printSchema()

print("Count:", df.count())
print("Columns:", df.columns)

# Filtering
engineers = df.filter(df.job == "Engineer")
engineers.show()

# Grouping and aggregation
job_stats = df.groupBy("job").agg(
    count("*").alias("count"),
    avg("age").alias("avg_age"),
    max("age").alias("max_age")
)
job_stats.show()
```

### Example 3: Reading and Writing Data

```python
# Reading CSV
df_csv = spark.read.option("header", "true").csv("data.csv")

# Reading JSON
df_json = spark.read.json("data.json")

# Reading Parquet
df_parquet = spark.read.parquet("data.parquet")

# Writing data
df.write.mode("overwrite").csv("output/csv_data")
df.write.mode("overwrite").json("output/json_data")
df.write.mode("overwrite").parquet("output/parquet_data")

# Writing with partitioning
df.write.mode("overwrite").partitionBy("job").parquet("output/partitioned_data")
```

### Example 4: SQL Operations

```python
# Register DataFrame as temporary view
df.createOrReplaceTempView("employees")

# SQL queries
result = spark.sql("""
    SELECT job,
           COUNT(*) as count,
           AVG(age) as avg_age,
           MAX(age) as max_age
    FROM employees
    GROUP BY job
    ORDER BY avg_age DESC
""")

result.show()

# Complex SQL with window functions
windowed_result = spark.sql("""
    SELECT name, age, job,
           ROW_NUMBER() OVER (PARTITION BY job ORDER BY age DESC) as rank,
           AVG(age) OVER (PARTITION BY job) as avg_job_age
    FROM employees
""")

windowed_result.show()
```

### Example 5: Working with Nested Data

```python
# Sample nested data
nested_data = [
    ("Alice", {"street": "123 Main St", "city": "NYC", "zip": "10001"}),
    ("Bob", {"street": "456 Oak Ave", "city": "LA", "zip": "90210"})
]

nested_schema = StructType([
    StructField("name", StringType(), True),
    StructField("address", StructType([
        StructField("street", StringType(), True),
        StructField("city", StringType(), True),
        StructField("zip", StringType(), True)
    ]), True)
])

nested_df = spark.createDataFrame(nested_data, nested_schema)

# Access nested fields
nested_df.select(
    "name",
    col("address.street").alias("street"),
    col("address.city").alias("city")
).show()

# Flatten nested structure
flattened_df = nested_df.select(
    "name",
    "address.street",
    "address.city",
    "address.zip"
)
flattened_df.show()
```

### Example 6: Data Transformation Pipeline

```python
# Sample sales data
sales_data = [
    ("2023-01-01", "Electronics", "Laptop", 1200.00, 2),
    ("2023-01-01", "Electronics", "Mouse", 25.00, 5),
    ("2023-01-02", "Clothing", "Shirt", 45.00, 3),
    ("2023-01-02", "Electronics", "Keyboard", 75.00, 2),
    ("2023-01-03", "Clothing", "Pants", 65.00, 1)
]

sales_schema = StructType([
    StructField("date", StringType(), True),
    StructField("category", StringType(), True),
    StructField("product", StringType(), True),
    StructField("price", DoubleType(), True),
    StructField("quantity", IntegerType(), True)
])

sales_df = spark.createDataFrame(sales_data, sales_schema)

# Data transformation pipeline
transformed_df = sales_df \
    .withColumn("date", to_date(col("date"), "yyyy-MM-dd")) \
    .withColumn("total_amount", col("price") * col("quantity")) \
    .withColumn("year", year(col("date"))) \
    .withColumn("month", month(col("date"))) \
    .withColumn("category_upper", upper(col("category")))

transformed_df.show()

# Aggregations
daily_sales = transformed_df.groupBy("date").agg(
    sum("total_amount").alias("daily_total"),
    count("*").alias("transaction_count"),
    avg("total_amount").alias("avg_transaction")
)

daily_sales.show()
```

### Example 7: Window Functions

```python
from pyspark.sql.window import Window

# Define window specification
window_spec = Window.partitionBy("category").orderBy(desc("total_amount"))

# Apply window functions
windowed_sales = transformed_df.withColumn(
    "rank", row_number().over(window_spec)
).withColumn(
    "running_total", sum("total_amount").over(
        Window.partitionBy("category")
        .orderBy("date")
        .rowsBetween(Window.unboundedPreceding, Window.currentRow)
    )
)

windowed_sales.show()
```

### Example 8: User-Defined Functions (UDFs)

```python
from pyspark.sql.functions import udf

# Define UDF
def categorize_price(price):
    if price < 50:
        return "Low"
    elif price < 200:
        return "Medium"
    else:
        return "High"

# Register UDF
categorize_price_udf = udf(categorize_price, StringType())

# Use UDF
df_with_categories = sales_df.withColumn(
    "price_category",
    categorize_price_udf(col("price"))
)

df_with_categories.show()
```

### Example 9: Caching and Persistence

```python
# Cache DataFrame
sales_df.cache()

# Different storage levels
from pyspark import StorageLevel

sales_df.persist(StorageLevel.MEMORY_AND_DISK)

# Check if cached
print("Is cached:", sales_df.is_cached)

# Unpersist
sales_df.unpersist()
```

### Example 10: Spark Streaming Example

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Create SparkSession for streaming
spark = SparkSession.builder \
    .appName("StreamingExample") \
    .getOrCreate()

# Define schema for streaming data
streaming_schema = StructType([
    StructField("timestamp", TimestampType(), True),
    StructField("user_id", StringType(), True),
    StructField("action", StringType(), True),
    StructField("value", DoubleType(), True)
])

# Read streaming data (example with file source)
streaming_df = spark.readStream \
    .format("json") \
    .schema(streaming_schema) \
    .option("path", "streaming_data/") \
    .load()

# Process streaming data
processed_stream = streaming_df \
    .withWatermark("timestamp", "10 minutes") \
    .groupBy(
        window(col("timestamp"), "5 minutes"),
        col("action")
    ) \
    .agg(
        count("*").alias("count"),
        sum("value").alias("total_value"),
        avg("value").alias("avg_value")
    )

# Output streaming results
query = processed_stream.writeStream \
    .outputMode("append") \
    .format("console") \
    .trigger(processingTime="30 seconds") \
    .start()

# Wait for termination
# query.awaitTermination()
```

### Best Practices

1. **Use DataFrames over RDDs** for better performance and optimization
2. **Cache frequently used datasets** to avoid recomputation
3. **Use appropriate file formats** (Parquet for analytics, Avro for schemas)
4. **Partition data properly** for better query performance
5. **Tune Spark configuration** based on cluster resources
6. **Monitor Spark UI** for performance optimization
7. **Use broadcast variables** for small lookup tables
8. **Avoid shuffles** when possible by using appropriate operations

### Performance Tuning Tips

```python
# 1. Optimize joins
# Use broadcast joins for small tables
from pyspark.sql.functions import broadcast
result = large_df.join(broadcast(small_df), "key")

# 2. Repartition data
df_repartitioned = df.repartition(4, "partition_key")

# 3. Coalesce partitions
df_coalesced = df.coalesce(2)

# 4. Use appropriate data types
df_optimized = df.select(
    col("id").cast("int"),
    col("amount").cast("decimal(10,2)")
)

# 5. Cache intermediate results
intermediate_df = df.filter(col("status") == "active")
intermediate_df.cache()
result1 = intermediate_df.groupBy("category").count()
result2 = intermediate_df.groupBy("region").sum("amount")
```

This comprehensive guide covers the essential aspects of Apache Spark, from basic concepts to practical examples. The PySpark examples demonstrate real-world scenarios and best practices for effective data processing with Spark.
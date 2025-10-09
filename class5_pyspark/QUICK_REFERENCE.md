# PySpark Quick Reference

Quick commands and code snippets for everyday PySpark development.

## Quick Start Commands

```bash
# Start the cluster
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f

# Stop cluster
docker compose stop

# Clean up
docker compose down
```

## Access Points

| Service | URL |
|---------|-----|
| Jupyter Notebook | http://localhost:8888 |
| Spark Master UI | http://localhost:8080 |
| Spark App UI | http://localhost:4040 |
| Worker 1 UI | http://localhost:8081 |
| Worker 2 UI | http://localhost:8082 |
| History Server | http://localhost:18080 |

## Initialize Spark Session

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("MyApp") \
    .master("spark://spark-master:7077") \
    .config("spark.executor.memory", "1g") \
    .config("spark.executor.cores", "1") \
    .getOrCreate()
```

## Common DataFrame Operations

```python
# Create DataFrame
df = spark.createDataFrame(data, ["col1", "col2"])

# Read CSV
df = spark.read.csv("/data/file.csv", header=True, inferSchema=True)

# Show data
df.show()
df.show(10, truncate=False)

# Schema
df.printSchema()

# Select
df.select("col1", "col2").show()

# Filter
df.filter(col("age") > 30).show()

# Group by
df.groupBy("category").count().show()

# Join
result = df1.join(df2, "key", "inner")

# Write
df.write.mode("overwrite").csv("/data/output.csv", header=True)
```

## Essential Imports

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, lit, when, concat,
    sum, avg, count, max, min,
    year, month, to_date,
    upper, lower, trim,
    explode, split
)
from pyspark.sql.window import Window
```

## Debugging

```python
# Show execution plan
df.explain()

# Count records
df.count()

# Sample data
df.sample(0.1).show()

# Check partitions
df.rdd.getNumPartitions()

# Cache for reuse
df.cache()
```

## Container Commands

```bash
# Execute command in container
docker exec -it pyspark-jupyter bash

# Check Python packages
docker exec pyspark-jupyter pip list

# View container logs
docker logs pyspark-jupyter

# Restart service
docker compose restart jupyter
```

## File Paths

Inside containers:
- Notebooks: `/notebooks/`
- Data files: `/data/`
- Apps: `/apps/`

On host:
- Notebooks: `./notebooks/`
- Data files: `./data/`
- Apps: `./apps/`

## Common Issues

| Problem | Solution |
|---------|----------|
| Can't access Jupyter | `docker compose restart jupyter` |
| PySpark not found | Use http://localhost:8888 (browser) |
| Out of memory | Increase Docker Desktop RAM allocation |
| Slow performance | Use `df.cache()` and broadcast joins |

## Documentation

- [README.md](README.md) - Complete documentation
- [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md) - Step-by-step setup guide
- [docs/EXAMPLES.md](docs/EXAMPLES.md) - PySpark code examples
- [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) - Problem solving guide

## Useful Links

- [PySpark API Docs](https://spark.apache.org/docs/latest/api/python/)
- [Spark SQL Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)
- [Docker Compose Docs](https://docs.docker.com/compose/)

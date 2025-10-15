# PySpark Advanced Examples

A comprehensive Docker-based PySpark setup with Jupyter Notebook containing advanced examples of joins, grouping, multidimensional data analysis, and nested column operations.

## Architecture

This setup includes:
- **Jupyter Notebook with PySpark** - All-in-one container with Spark, Python, and Jupyter
- **Spark in Local Mode** - Utilizes all available cores for parallel processing
- **Interactive Development** - Full PySpark environment accessible via web browser

## Prerequisites

- Docker Desktop installed and running
- At least 6GB of available RAM
- Docker Compose

## Quick Start

### 1. Start Jupyter

```bash
# Start the Jupyter container
docker compose up -d

# Check that the service is running
docker compose ps
```

### 2. Access Jupyter Notebook

Once the service is running:

- **Jupyter Notebook**: http://localhost:8888
  - No password required (configured for development)
  - Open `work/pyspark_advanced_examples.ipynb` to get started

- **Spark Application UI**: http://localhost:4040
  - Available when a Spark application is running
  - Monitor job progress, stages, and execution details

### 3. Run the Examples

1. Open Jupyter at http://localhost:8888
2. Navigate to the `work` directory
3. Open `pyspark_advanced_examples.ipynb`
4. Run the cells sequentially to see the examples in action

### 4. Stop the Container

```bash
# Stop the service
docker compose down

# Stop and remove volumes (clears all data)
docker compose down -v
```

## Notebook Content

The notebook contains **9 comprehensive examples** organized into three sections:

### Section 1: Joining & Grouping (3 Examples)

1. **E-Commerce Order Analysis**
   - Multi-table joins (customers, orders, order_items, products, categories)
   - Complex aggregations with groupBy
   - Customer and category analytics

2. **Employee Department Analysis**
   - Self-joins for employee-manager hierarchy
   - Window functions for salary rankings
   - Department performance metrics

3. **Student Course Enrollment**
   - Multi-table joins across students, courses, instructors, and enrollments
   - Student performance analytics
   - Instructor teaching effectiveness analysis

### Section 2: Multidimensional DataFrames (3 Examples)

1. **Sales Data Cube**
   - Rollup operations for hierarchical aggregations
   - Cube operations for all dimension combinations
   - Pivot tables for product-region analysis

2. **Weather Data Analysis**
   - Multi-dimensional weather patterns across locations and seasons
   - Cube analysis with multiple dimensions
   - Temperature range classifications

3. **Financial Portfolio Analysis**
   - Complete cube across quarter, asset type, sector, and risk level
   - Hierarchical rollup for portfolio metrics
   - Risk-return matrix with pivots

### Section 3: Nested Columns (3 Examples)

1. **E-Commerce Orders with Nested Structures**
   - Deeply nested customer and shipping information
   - Array operations with order items
   - Exploding and re-nesting data structures

2. **Social Media Posts**
   - Complex nested author profiles and engagement metrics
   - Nested arrays of comments with replies
   - Hashtag and reaction analysis

3. **IoT Sensor Data**
   - Nested device information and location data
   - Arrays of sensor readings and events
   - Device health reports with nested structures

## PySpark Concepts Demonstrated

### Joins & Grouping
- Inner, left, and self joins
- groupBy with multiple aggregation functions
- Window functions (rank, dense_rank, percent_rank)
- collect_list, collect_set for array aggregations

### Multidimensional Analysis
- `rollup()` - Hierarchical aggregations
- `cube()` - All possible dimension combinations
- `pivot()` - Transforming rows to columns
- Multi-level grouping and aggregations

### Nested Data Operations
- Extracting nested fields with dot notation
- `explode()` - Converting arrays to rows
- `struct()` - Creating nested structures
- `collect_list()` with struct for re-nesting
- Working with arrays and maps

## Docker Compose Configuration

### Service

#### Jupyter with PySpark
- Image: `jupyter/all-spark-notebook:latest`
- Ports: 8888 (Notebook), 4040 (Spark UI), 8080 (alternate)
- Spark Mode: Local with all available cores
- Pre-configured with PySpark and all necessary libraries

### Volumes

- `./notebooks` - Mounted to Jupyter for notebook storage
- `./data` - Shared directory for data files

## Troubleshooting

### Service Won't Start

```bash
# Check logs
docker compose logs jupyter

# Restart service
docker compose restart
```

### Can't Connect to Jupyter

1. Check if Jupyter is running: `docker compose ps`
2. View Jupyter logs: `docker compose logs jupyter`
3. Ensure port 8888 is not already in use

### Out of Memory Errors

1. Increase Docker Desktop memory allocation (Settings > Resources)
2. Reduce data size in examples
3. Restart the kernel in Jupyter

### Notebook Kernel Dies

This usually indicates memory issues. Try:
1. Restart the kernel
2. Reduce data size in examples
3. Run fewer examples in a single session
4. Increase Docker Desktop memory allocation

## Advanced Configuration

### Customize Spark Configuration

Edit the notebook's SparkSession initialization:

```python
spark = SparkSession.builder \
    .appName("My Application") \
    .master("local[*]") \
    .config("spark.driver.memory", "4g") \
    .config("spark.sql.shuffle.partitions", "4") \
    .getOrCreate()
```

### Enable Authentication

For production use, edit `docker-compose.yml`:

```yaml
command: start-notebook.sh --NotebookApp.token='your-secure-token'
```

## Learning Resources

- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [PySpark API Reference](https://spark.apache.org/docs/latest/api/python/)
- [Spark SQL Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)
- [Jupyter Docker Stacks](https://jupyter-docker-stacks.readthedocs.io/)

## Project Structure

```
class6_pyspark/
├── docker-compose.yml          # Docker Compose configuration
├── README.md                   # This file
├── notebooks/                  # Jupyter notebooks
│   └── pyspark_advanced_examples.ipynb
└── data/                       # Data files (if any)
```

## Performance Notes

- Spark runs in **local mode** using all available CPU cores
- Default configuration uses 4 shuffle partitions (optimized for local mode)
- Driver memory is set to 4GB (can be adjusted in notebook)
- All processing happens within a single container

## License

This project is for educational purposes.

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review Docker Compose logs
3. Consult Apache Spark documentation

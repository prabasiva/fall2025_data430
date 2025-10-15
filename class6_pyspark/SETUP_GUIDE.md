# PySpark Setup Guide

## Current Status

You have **two Docker Compose configurations** available:

### Option 1: Single Container (Currently Running) ✅
**File:** `docker-compose.yml`
**Status:** Active and working
**Access:** http://localhost:8888

This setup uses Jupyter with built-in Spark running in local mode.

**Pros:**
- Fast to start
- Simple configuration
- No Python version conflicts
- Perfect for learning and development
- Uses all available CPU cores

**Cons:**
- Not a true distributed cluster
- No separate master/worker nodes to visualize

---

### Option 2: Master-Worker Cluster
**File:** `docker-compose-cluster.yml`
**Status:** Available (images may need to download)

This setup creates a true Spark cluster with:
- 1 Spark Master node
- 2 Spark Worker nodes (2GB RAM, 2 cores each)
- 1 Jupyter Notebook

**Pros:**
- True distributed Spark cluster
- See master/worker architecture
- Spark Master UI available
- More realistic production-like setup

**Cons:**
- Larger Docker images (takes time to download)
- More complex configuration
- Requires more system resources

---

## How to Switch Between Setups

### Currently Using: Single Container

To switch to the **Master-Worker Cluster**:

```bash
# Stop current setup
docker compose down

# Start cluster setup
docker compose -f docker-compose-cluster.yml up -d

# Check status
docker compose -f docker-compose-cluster.yml ps

# View logs
docker compose -f docker-compose-cluster.yml logs -f
```

**Access Points (Cluster Mode):**
- Jupyter Notebook: http://localhost:8888
- Spark Master UI: http://localhost:8080
- Spark Application UI: http://localhost:4040 (when jobs are running)

### Switch Back to Single Container:

```bash
# Stop cluster
docker compose -f docker-compose-cluster.yml down

# Start single container
docker compose up -d
```

---

## Notebook Configuration

### For Single Container (Current)
The notebook is configured for **local mode**:
```python
spark = SparkSession.builder \
    .appName("PySpark Advanced Examples") \
    .master("local[*]") \
    .config("spark.sql.shuffle.partitions", "4") \
    .getOrCreate()
```

### For Master-Worker Cluster
Update the notebook's first cell to:
```python
spark = SparkSession.builder \
    .appName("PySpark Advanced Examples") \
    .master("spark://spark-master:7077") \
    .config("spark.executor.memory", "2g") \
    .config("spark.executor.cores", "2") \
    .getOrCreate()
```

---

## Troubleshooting

### Cluster Images Still Downloading

If you try to start the cluster and it takes a long time:

```bash
# Check download progress
docker compose -f docker-compose-cluster.yml pull

# This will show download progress for all images
```

The cluster images are large (~500MB+ each). Once downloaded, they start quickly.

### Port Conflicts

If you get port conflicts:
1. Make sure the other setup is stopped: `docker compose down`
2. Check for other services: `docker ps`
3. Kill any conflicting processes using ports 8888, 8080, 4040, 7077

### Python Version Mismatch (Cluster)

If you encounter Python version errors in cluster mode:
- The configuration uses compatible images (Apache Spark 3.4.1 + Jupyter Spark 3.4.1)
- Both use Python 3.11
- This should work without conflicts

---

## Recommendations

### For Learning PySpark Concepts
**Use:** Single Container (`docker-compose.yml`)
- Faster iteration
- Simpler debugging
- Perfect for the examples in the notebook

### For Understanding Cluster Architecture
**Use:** Master-Worker Cluster (`docker-compose-cluster.yml`)
- See how jobs are distributed
- Monitor worker nodes
- View master UI
- More realistic for production understanding

---

## Files in This Directory

```
class6_pyspark/
├── docker-compose.yml              # Single container (currently active)
├── docker-compose-cluster.yml      # Master-worker cluster
├── docker-compose.yml.backup       # Original backup
├── SETUP_GUIDE.md                  # This file
├── README.md                       # Main documentation
├── notebooks/
│   └── pyspark_advanced_examples.ipynb
└── data/
```

---

## Quick Commands Reference

```bash
# Single Container
docker compose up -d                 # Start
docker compose down                  # Stop
docker compose logs -f              # View logs
docker compose ps                   # Check status

# Master-Worker Cluster
docker compose -f docker-compose-cluster.yml up -d      # Start
docker compose -f docker-compose-cluster.yml down       # Stop
docker compose -f docker-compose-cluster.yml logs -f    # View logs
docker compose -f docker-compose-cluster.yml ps         # Check status
```

---

## Next Steps

1. ✅ **Current Setup Works** - You can start using the notebook immediately
2. Open http://localhost:8888
3. Navigate to `work/pyspark_advanced_examples.ipynb`
4. Run the examples

When you want to try the cluster setup, follow the "Switch to Master-Worker Cluster" instructions above.

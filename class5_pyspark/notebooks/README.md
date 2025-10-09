# PySpark Jupyter Notebooks

## Quick Start

1. **Open Jupyter**: http://localhost:8888
2. **Open**: `test_pyspark.ipynb`
3. **Run cells**: Shift+Enter to run each cell

## Troubleshooting

### If cells don't show output:

1. **Check kernel is running**: Look for "Python 3 (ipykernel)" in top-right
2. **Restart kernel**: Kernel menu → Restart Kernel
3. **Run cells one by one**: Don't run all at once first time

### If Spark connection fails:

```python
# Use local mode instead of cluster
spark = SparkSession.builder \
    .appName("Test") \
    .master("local[*]") \
    .getOrCreate()
```

### Check cluster status:
- Master: http://localhost:8080
- Workers: http://localhost:8081, http://localhost:8082

## Common Issues

**No output displayed**:
- Make sure to use `print()` or `.show()` to display results
- Check that cell has executed (number appears in brackets `[1]`)

**Cell stuck executing**:
- Restart kernel: Kernel → Restart
- Check Spark Master UI for errors

**Connection timeout**:
- Verify containers running: `docker ps`
- Check master is healthy: `docker logs pyspark-master`

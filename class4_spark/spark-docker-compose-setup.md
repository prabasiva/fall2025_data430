# Spark Docker Compose Setup Guide

## Docker Compose Configuration

Create a file named `docker-compose.yml` with the following content:

```yaml
version: '3.8'

services:
  spark-master:
    image: apache/spark:3.5.0
    container_name: spark-master
    hostname: spark-master
    ports:
      - "8080:8080"  # Spark Master Web UI
      - "7077:7077"  # Spark Master Port
      - "4040:4040"  # Spark Application UI (when running)
    environment:
      - SPARK_MODE=master
      - SPARK_MASTER_HOST=spark-master
      - SPARK_MASTER_PORT=7077
      - SPARK_MASTER_WEBUI_PORT=8080
      - SPARK_DAEMON_MEMORY=1g
    volumes:
      - ./data:/data
      - ./apps:/apps
      - spark-logs:/opt/spark/logs
    networks:
      - spark-network
    command: >
      bash -c "
        /opt/spark/sbin/start-master.sh &&
        tail -f /opt/spark/logs/spark--org.apache.spark.deploy.master.Master-*.out
      "
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  spark-worker-1:
    image: apache/spark:3.5.0
    container_name: spark-worker-1
    hostname: spark-worker-1
    depends_on:
      spark-master:
        condition: service_healthy
    ports:
      - "8081:8081"  # Worker 1 Web UI
    environment:
      - SPARK_MODE=worker
      - SPARK_MASTER=spark://spark-master:7077
      - SPARK_WORKER_WEBUI_PORT=8081
      - SPARK_WORKER_PORT=7078
      - SPARK_WORKER_CORES=2
      - SPARK_WORKER_MEMORY=2g
      - SPARK_DAEMON_MEMORY=1g
    volumes:
      - ./data:/data
      - ./apps:/apps
      - spark-logs:/opt/spark/logs
    networks:
      - spark-network
    command: >
      bash -c "
        /opt/spark/sbin/start-worker.sh spark://spark-master:7077 &&
        tail -f /opt/spark/logs/spark--org.apache.spark.deploy.worker.Worker-*.out
      "
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8081"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  spark-worker-2:
    image: apache/spark:3.5.0
    container_name: spark-worker-2
    hostname: spark-worker-2
    depends_on:
      spark-master:
        condition: service_healthy
    ports:
      - "8082:8082"  # Worker 2 Web UI
    environment:
      - SPARK_MODE=worker
      - SPARK_MASTER=spark://spark-master:7077
      - SPARK_WORKER_WEBUI_PORT=8082
      - SPARK_WORKER_PORT=7079
      - SPARK_WORKER_CORES=2
      - SPARK_WORKER_MEMORY=2g
      - SPARK_DAEMON_MEMORY=1g
    volumes:
      - ./data:/data
      - ./apps:/apps
      - spark-logs:/opt/spark/logs
    networks:
      - spark-network
    command: >
      bash -c "
        /opt/spark/sbin/start-worker.sh spark://spark-master:7077 &&
        tail -f /opt/spark/logs/spark--org.apache.spark.deploy.worker.Worker-*.out
      "
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8082"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Optional: Spark History Server
  spark-history:
    image: apache/spark:3.5.0
    container_name: spark-history
    hostname: spark-history
    depends_on:
      - spark-master
    ports:
      - "18080:18080"  # History Server Web UI
    environment:
      - SPARK_HISTORY_OPTS=-Dspark.history.fs.logDirectory=/tmp/spark-events
      - SPARK_DAEMON_MEMORY=1g
    volumes:
      - spark-events:/tmp/spark-events
      - spark-logs:/opt/spark/logs
    networks:
      - spark-network
    command: >
      bash -c "
        mkdir -p /tmp/spark-events &&
        /opt/spark/sbin/start-history-server.sh &&
        tail -f /opt/spark/logs/spark--org.apache.spark.deploy.history.HistoryServer-*.out
      "

networks:
  spark-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.28.0.0/16

volumes:
  spark-logs:
  spark-events:
```

## Additional Configuration Files

### 1. Environment Variables File (.env)

Create a `.env` file for easy configuration:

```env
# .env
SPARK_VERSION=3.5.0
SPARK_MASTER_MEMORY=1g
SPARK_WORKER_MEMORY=2g
SPARK_WORKER_CORES=2
SPARK_DRIVER_MEMORY=1g
```

### 2. Directory Structure Setup

Create necessary directories:

```bash
# Create necessary directories
mkdir -p data apps

# Set permissions
chmod -R 777 data apps
```

### 3. Custom Spark Configuration (Optional)

Create `spark-defaults.conf`:

```properties
# spark-defaults.conf
spark.master                     spark://spark-master:7077
spark.eventLog.enabled           true
spark.eventLog.dir               /tmp/spark-events
spark.history.fs.logDirectory    /tmp/spark-events
spark.serializer                 org.apache.spark.serializer.KryoSerializer
spark.sql.adaptive.enabled       true
spark.sql.adaptive.coalescePartitions.enabled true
```

To use this configuration, add it to the volumes section in docker-compose.yml:
```yaml
volumes:
  - ./spark-defaults.conf:/opt/spark/conf/spark-defaults.conf
```

## Usage Commands

### Starting the Cluster

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Scale workers (add more workers)
docker-compose up -d --scale spark-worker-2=3
```

### Submitting Spark Applications

```bash
# Submit a PySpark application
docker exec -it spark-master spark-submit \
  --master spark://spark-master:7077 \
  --deploy-mode client \
  --driver-memory 1g \
  --executor-memory 1g \
  --executor-cores 1 \
  /apps/your-app.py

# Run Spark shell
docker exec -it spark-master spark-shell \
  --master spark://spark-master:7077

# Run PySpark shell
docker exec -it spark-master pyspark \
  --master spark://spark-master:7077
```

### Example PySpark Application

Save this as `apps/test_spark.py`:

```python
from pyspark.sql import SparkSession
import time

# Create Spark session
spark = SparkSession.builder \
    .appName("TestSparkCluster") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# Create sample data
data = [(i, f"name_{i}", i * 100) for i in range(1, 1001)]
columns = ["id", "name", "value"]

# Create DataFrame
df = spark.createDataFrame(data, columns)

# Perform operations
result = df.groupBy("id").sum("value").count()
print(f"Total records: {result}")

# Keep application running to view in UI
time.sleep(60)

spark.stop()
```

## Monitoring

Access the web interfaces:
- **Spark Master UI**: http://localhost:8080
- **Worker 1 UI**: http://localhost:8081
- **Worker 2 UI**: http://localhost:8082
- **Spark History Server**: http://localhost:18080
- **Application UI** (when running): http://localhost:4040

## Stopping the Cluster

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## Production Considerations

For production environments, consider:

### 1. Resource Limits
```yaml
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 4G
    reservations:
      cpus: '1'
      memory: 2G
```

### 2. Additional Considerations
- **Persistent storage** for checkpointing and logs
- **Security** configurations (authentication, encryption)
- **Network policies** and firewall rules
- **Monitoring** with Prometheus/Grafana
- **Load balancing** for high availability

## Troubleshooting

### Common Issues and Solutions

1. **Workers not connecting to master**
   - Ensure the master is fully started before workers
   - Check firewall rules for port 7077
   - Verify network connectivity between containers

2. **Out of memory errors**
   - Increase `SPARK_WORKER_MEMORY` and `SPARK_DAEMON_MEMORY`
   - Adjust Docker's memory limits
   - Configure appropriate executor memory in spark-submit

3. **Port conflicts**
   - Change port mappings in docker-compose.yml
   - Ensure no other services are using ports 8080-8082, 7077, 4040, 18080

4. **Logs not visible**
   - Check volume permissions
   - Ensure log directories exist
   - Review Docker logs: `docker logs spark-master`

## Quick Start Guide

1. Save the docker-compose.yml file
2. Create data and apps directories
3. Run `docker-compose up -d`
4. Access Spark Master UI at http://localhost:8080
5. Submit your first application!

This setup provides a fully functional Spark cluster suitable for development and testing. Adjust memory and CPU settings based on your available resources.
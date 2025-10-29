# Envoy API Gateway - Command Reference

Quick reference for managing and testing the Envoy API Gateway.

## Docker Compose Commands

### Start All Services
```bash
docker compose up -d
```

### Stop All Services
```bash
docker compose down
```

### View Logs
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f envoy-proxy-1
docker compose logs -f control-plane
docker compose logs -f graphql-api
```

### Check Status
```bash
docker compose ps
```

### Restart Service
```bash
docker compose restart envoy-proxy-1
```

### Scale Services
```bash
# Scale Envoy proxies
docker compose up -d --scale envoy-proxy-1=5

# Scale backend services
docker compose up -d --scale rest-api=3
```

## Testing Commands

### Run All Tests
```bash
./scripts/test-gateway.sh
```

### Test REST API
```bash
# Get categories
curl http://localhost:10000/api/categories

# Get products by category
curl http://localhost:10000/api/products/category/Electronics

# Get top products by sales
curl "http://localhost:10000/api/products/top-sales/Sports?limit=5"
```

### Test GraphQL API
```bash
# Simple query
curl -X POST http://localhost:10000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ hello }"}'

# Get users
curl -X POST http://localhost:10000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ users { name email } }"}'

# Nested query
curl -X POST http://localhost:10000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ user(id: 1) { name posts { title likes } } }"}'

# Mutation
curl -X POST http://localhost:10000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { createPost(input: {title: \"Test\", content: \"Content\", authorId: 1, published: true}) { id title } }"}'
```

### Test Multiple Proxies
```bash
# Test Proxy 1
curl http://localhost:10000/

# Test Proxy 2
curl http://localhost:10002/

# Test Proxy 3
curl http://localhost:10004/
```

## Control Plane Commands

### Get Status
```bash
curl http://localhost:8080/status
```

### List Services
```bash
curl http://localhost:8080/services
```

### List Routes
```bash
curl http://localhost:8080/routes
```

### List Registered Proxies
```bash
curl http://localhost:8080/proxies
```

### Add New Service
```bash
curl -X POST http://localhost:8080/services/add \
  -H "Content-Type: application/json" \
  -d '{
    "name": "new-service",
    "address": "new-service",
    "port": 8080,
    "protocol": "http",
    "health_check_path": "/health"
  }'
```

### Reload Configuration
```bash
curl -X POST http://localhost:8080/config/reload
```

## Envoy Admin Commands

### View Statistics
```bash
# Proxy 1
curl http://localhost:9901/stats

# Proxy 2
curl http://localhost:9902/stats

# Proxy 3
curl http://localhost:9903/stats
```

### View Prometheus Metrics
```bash
curl http://localhost:9901/stats/prometheus
```

### View Cluster Status
```bash
curl http://localhost:9901/clusters
```

### View Configuration
```bash
curl http://localhost:9901/config_dump
```

### View Listeners
```bash
curl http://localhost:9901/listeners
```

### Check Health
```bash
curl http://localhost:9901/ready
```

## Monitoring Commands

### Check Backend Health via Envoy
```bash
curl -s http://localhost:9901/clusters | grep health_flags
```

### View Request Statistics
```bash
curl -s http://localhost:9901/stats | grep http.ingress_http
```

### View Upstream Statistics
```bash
curl -s http://localhost:9901/stats | grep cluster.rest_service
curl -s http://localhost:9901/stats | grep cluster.graphql_service
curl -s http://localhost:9901/stats | grep cluster.grpc_service
```

## Debugging Commands

### View Envoy Logs in Real-time
```bash
docker compose logs -f envoy-proxy-1 | grep -E "HTTP|error"
```

### View Backend Logs
```bash
docker compose logs -f rest-api
docker compose logs -f graphql-api
docker compose logs -f grpc-api
```

### Check Container Resource Usage
```bash
docker stats
```

### Inspect Network
```bash
docker network inspect envoy-gateway_api-network
```

### Execute Command in Container
```bash
docker compose exec envoy-proxy-1 sh
docker compose exec control-plane sh
```

## Load Testing Commands

### Simple Load Test (using ab)
```bash
# Install apache-bench if not available
# brew install httpd (macOS)

# Test REST endpoint
ab -n 1000 -c 10 http://localhost:10000/api/categories

# Test GraphQL endpoint
echo '{"query": "{ hello }"}' > query.json
ab -n 1000 -c 10 -p query.json -T application/json \
  http://localhost:10000/graphql
```

### Load Test with hey
```bash
# Install hey
# go install github.com/rakyll/hey@latest

# Test REST
hey -n 1000 -c 50 http://localhost:10000/api/categories

# Test all three proxies
hey -n 1000 -c 50 http://localhost:10000/
hey -n 1000 -c 50 http://localhost:10002/
hey -n 1000 -c 50 http://localhost:10004/
```

## Troubleshooting Commands

### Check if Ports are Open
```bash
lsof -i :10000
lsof -i :10002
lsof -i :10004
lsof -i :8080
```

### Test Network Connectivity
```bash
# From host to container
docker compose exec rest-api curl http://localhost:8000/

# Between containers
docker compose exec envoy-proxy-1 wget -O- http://rest-api:8000/
```

### View Container Configuration
```bash
docker compose config
```

### Validate YAML Files
```bash
# Validate docker-compose.yaml
docker compose config --quiet

# Validate Envoy config (requires envoy binary)
envoy --mode validate -c config/envoy-proxy.yaml
```

## Cleanup Commands

### Stop and Remove All Containers
```bash
docker compose down
```

### Stop and Remove with Volumes
```bash
docker compose down -v
```

### Remove All Images
```bash
docker compose down --rmi all
```

### Full Cleanup
```bash
docker compose down -v --rmi all --remove-orphans
```

## Performance Tuning Commands

### Adjust Worker Threads (in envoy-proxy.yaml)
```yaml
concurrency: 4  # Number of worker threads
```

### Adjust Connection Limits
```yaml
circuit_breakers:
  thresholds:
    max_connections: 1000
    max_pending_requests: 1000
```

### Adjust Timeout Settings
```yaml
route:
  cluster: rest_service
  timeout: 30s
  idle_timeout: 60s
```

## Backup and Restore

### Backup Configuration
```bash
# Backup all configs
tar -czf envoy-gateway-backup.tar.gz \
  config/ \
  control-plane/ \
  docker-compose.yaml

# Backup with timestamp
tar -czf "envoy-gateway-backup-$(date +%Y%m%d-%H%M%S).tar.gz" \
  config/ control-plane/ docker-compose.yaml
```

### Restore Configuration
```bash
tar -xzf envoy-gateway-backup.tar.gz
docker compose up -d
```

## Production Deployment

### Build for Production
```bash
docker compose -f docker-compose.yaml \
  -f docker-compose.prod.yaml up -d
```

### Push Images to Registry
```bash
# Tag images
docker tag envoy-gateway-rest-api:latest registry.example.com/rest-api:v1.0.0
docker tag envoy-gateway-graphql-api:latest registry.example.com/graphql-api:v1.0.0
docker tag envoy-gateway-grpc-api:latest registry.example.com/grpc-api:v1.0.0

# Push to registry
docker push registry.example.com/rest-api:v1.0.0
docker push registry.example.com/graphql-api:v1.0.0
docker push registry.example.com/grpc-api:v1.0.0
```

## Quick Reference

```bash
# Start gateway
docker compose up -d

# Test everything
./scripts/test-gateway.sh

# View logs
docker compose logs -f

# Check health
curl http://localhost:9901/clusters | grep health

# Stop gateway
docker compose down
```

---

**Tip**: Save frequently used commands as shell aliases:
```bash
alias egw-start="cd ~/envoy-gateway && docker compose up -d"
alias egw-stop="cd ~/envoy-gateway && docker compose down"
alias egw-test="cd ~/envoy-gateway && ./scripts/test-gateway.sh"
alias egw-logs="cd ~/envoy-gateway && docker compose logs -f"
```

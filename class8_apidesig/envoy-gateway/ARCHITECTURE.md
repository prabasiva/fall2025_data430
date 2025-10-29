# Envoy API Gateway - Architecture Documentation

## Overview

This project implements a **production-grade API Gateway** using Envoy Proxy with a custom control plane. It demonstrates modern cloud-native architecture patterns including service mesh concepts, dynamic configuration management, and high availability.

## System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    Control Plane                              │
│         (Dynamic Configuration Management)                    │
│               Port: 8080                                      │
└───────────────────────┬──────────────────────────────────────┘
                        │
                        │ xDS Protocol / REST API
                        │ (Configuration Updates)
                        │
        ┌───────────────┼───────────────┐
        │               │               │
┌───────▼────────┐ ┌────▼───────┐ ┌────▼───────┐
│  Envoy Proxy 1 │ │ Envoy Proxy 2│ │ Envoy Proxy 3│
│                │ │              │ │             │
│  HTTP: 10000   │ │  HTTP: 10002 │ │ HTTP: 10004 │
│  gRPC: 10001   │ │  gRPC: 10003 │ │ gRPC: 10005 │
│  Admin: 9901   │ │  Admin: 9902 │ │ Admin: 9903 │
└───────┬────────┘ └────┬───────┘ └────┬───────┘
        │               │              │
        │  Load Balancing & Health Checking │
        │               │              │
 ┌──────┴───────────────┴──────────────┴─────┐
 │                                            │
 │        Backend Services Network            │
 │                                            │
 └──┬──────────────┬─────────────────┬────────┘
    │              │                 │
┌───▼────┐   ┌─────▼──────┐   ┌─────▼────┐
│REST API│   │GraphQL API │   │ gRPC API │
│        │   │            │   │          │
│ :8000  │   │   :8000    │   │  :50051  │
│        │   │            │   │          │
│Products│   │Users/Posts │   │   User   │
│  CSV   │   │ Comments   │   │  Service │
└────────┘   └────────────┘   └──────────┘
```

## Components

### 1. Envoy Proxy Layer

**Purpose**: Edge proxy and API gateway

**Features**:
- Protocol translation (HTTP/1.1, HTTP/2, gRPC)
- Load balancing (Round Robin)
- Health checking
- Request routing
- Observability (metrics, logging, tracing)

**Configuration**:
- Static configuration via YAML file
- Dynamic configuration via xDS protocol
- Service discovery
- Circuit breaking

**Instances**: 3 proxies for high availability

### 2. Control Plane

**Purpose**: Central configuration management

**Responsibilities**:
- Service registration and discovery
- Route configuration
- Health policy management
- Configuration versioning
- Proxy instance tracking

**API Endpoints**:
```
GET  /status              - System status
GET  /services            - List all services
POST /services/add        - Register new service
DELETE /services/{name}   - Remove service
GET  /routes              - List routes
POST /routes/add          - Add route
GET  /proxies             - List proxy instances
POST /proxies/register    - Register proxy
POST /config/reload       - Reload configuration
```

**Technology**: Python FastAPI

### 3. Backend Services

#### REST API Service
- **Port**: 8000
- **Protocol**: HTTP/1.1
- **Data**: Product inventory (CSV-based)
- **Endpoints**:
  - `/api/categories`
  - `/api/products/*`
  - `/health`

#### GraphQL API Service
- **Port**: 8000
- **Protocol**: HTTP/1.1 (with GraphQL)
- **Data**: Users, Posts, Comments (in-memory)
- **Features**:
  - Query and Mutation support
  - Nested relationships
  - Interactive playground

#### gRPC API Service
- **Port**: 50051
- **Protocol**: HTTP/2 (gRPC)
- **Features**:
  - Unary RPC
  - Server streaming
  - Client streaming
  - Bidirectional streaming

## Traffic Flow

### HTTP/REST Request Flow

```
Client Request
    ↓
Envoy Listener (:10000)
    ↓
HTTP Connection Manager
    ↓
Route Matching (/api/*)
    ↓
Cluster Selection (rest_service)
    ↓
Load Balancer (Round Robin)
    ↓
Health Check (if needed)
    ↓
Backend Service (REST API :8000)
    ↓
Response
    ↓
Client
```

### GraphQL Request Flow

```
Client Request (POST /graphql)
    ↓
Envoy Listener (:10000)
    ↓
HTTP Connection Manager
    ↓
Route Matching (/graphql)
    ↓
CORS Filter
    ↓
Cluster Selection (graphql_service)
    ↓
Backend Service (GraphQL API :8000)
    ↓
Response
    ↓
Client
```

### gRPC Request Flow

```
gRPC Client Request
    ↓
Envoy Listener (:10001)
    ↓
HTTP/2 Connection Manager
    ↓
gRPC Stats Filter
    ↓
gRPC Web Filter
    ↓
Cluster Selection (grpc_service)
    ↓
Backend Service (gRPC API :50051)
    ↓
gRPC Response
    ↓
Client
```

## Configuration Management

### Static Configuration
- **File**: `config/envoy-proxy.yaml`
- **Content**:
  - Listeners (ports and protocols)
  - Clusters (backend services)
  - Routes (path-based routing)
  - Health checks
  - Admin interface

### Dynamic Configuration (xDS)
- **Protocol**: gRPC-based xDS
- **Types**:
  - **LDS** (Listener Discovery Service)
  - **RDS** (Route Discovery Service)
  - **CDS** (Cluster Discovery Service)
  - **EDS** (Endpoint Discovery Service)

### Configuration Updates
1. Control plane receives update request
2. Version number incremented
3. New configuration generated
4. All proxies notified via xDS
5. Proxies fetch and apply new config
6. Old connections drained gracefully

## High Availability

### Multiple Proxy Instances
- 3 Envoy instances running simultaneously
- Each can handle full traffic independently
- External load balancer distributes traffic

### Health Checking
- **Service Level**: Envoy checks backend health
- **Container Level**: Docker health checks
- **Proxy Level**: Admin endpoint monitoring

### Failover
- Unhealthy backends automatically removed
- Traffic redistributed to healthy instances
- Automatic recovery when health restored

## Load Balancing

### Strategy: Round Robin
- Distributes requests evenly
- Simple and effective
- No session affinity needed

### Alternative Strategies (Configurable)
- **Least Request**: Send to least loaded
- **Random**: Random selection
- **Ring Hash**: Consistent hashing
- **Maglev**: Faster consistent hashing

## Observability

### Metrics
- Request count per service
- Latency percentiles (p50, p90, p99)
- Error rates
- Connection statistics
- Upstream health status

**Access**: `http://localhost:9901/stats/prometheus`

### Logging
- Access logs for all requests
- Structured JSON format
- Includes:
  - Request method and path
  - Response status
  - Duration
  - Upstream service
  - Client IP

### Admin Interface
- `/stats` - Detailed statistics
- `/clusters` - Cluster status
- `/config_dump` - Current configuration
- `/health` - Health check endpoint
- `/ready` - Readiness probe

## Security Considerations

### Implemented
- CORS support for GraphQL
- Health check endpoints
- Admin interface access control (localhost only)

### Production Recommendations
1. **TLS/SSL**:
   - Enable HTTPS for external traffic
   - mTLS for service-to-service

2. **Authentication**:
   - JWT validation
   - API key management
   - OAuth2 integration

3. **Rate Limiting**:
   - Per-client rate limits
   - Per-route limits
   - Global limits

4. **Access Control**:
   - IP whitelisting
   - Role-based access
   - Request validation

## Scalability

### Horizontal Scaling

**Envoy Proxies**:
```bash
docker-compose up -d --scale envoy-proxy-1=10
```

**Backend Services**:
```bash
docker-compose up -d --scale rest-api=5
docker-compose up -d --scale graphql-api=3
docker-compose up -d --scale grpc-api=4
```

### Performance Tuning
- Connection pooling
- Keep-alive settings
- Buffer sizes
- Worker threads
- Circuit breakers

## Deployment Patterns

### Development
```
docker-compose up
```

### Production
1. **Kubernetes**:
   - Envoy as sidecar
   - Control plane as deployment
   - Service mesh (Istio, Linkerd)

2. **Cloud**:
   - AWS App Mesh
   - Google Traffic Director
   - Azure Service Fabric Mesh

3. **Bare Metal**:
   - Systemd services
   - Configuration management (Ansible, Chef)
   - Consul for service discovery

## Monitoring and Alerting

### Key Metrics to Monitor
1. **Request Rate**:
   - Requests per second per service
   - Growth trends

2. **Latency**:
   - p50, p90, p99 percentiles
   - Spikes and anomalies

3. **Error Rate**:
   - 4xx errors (client)
   - 5xx errors (server)
   - Timeout errors

4. **Resource Usage**:
   - CPU usage
   - Memory usage
   - Connection count

### Alert Thresholds
- Error rate > 1%
- Latency p99 > 1000ms
- Health check failures
- Memory usage > 80%

## Advanced Features

### Circuit Breaking
Prevents cascade failures:
```yaml
circuit_breakers:
  thresholds:
    - priority: DEFAULT
      max_connections: 1000
      max_pending_requests: 1000
      max_requests: 1000
      max_retries: 3
```

### Retry Policy
Automatic retries for failed requests:
```yaml
retry_policy:
  retry_on: "5xx"
  num_retries: 3
  per_try_timeout: 3s
```

### Timeout Configuration
- Connection timeout: 5s
- Request timeout: 30s
- Idle timeout: 60s

## Troubleshooting

### Common Issues

**1. Service Unavailable (503)**
- Check backend service health
- Verify network connectivity
- Review Envoy admin `/clusters`

**2. Configuration Not Applying**
- Check configuration syntax
- Verify control plane logs
- Force reload via API

**3. High Latency**
- Check backend performance
- Review connection pooling
- Analyze request patterns

### Debug Commands
```bash
# View Envoy config
curl http://localhost:9901/config_dump

# Check cluster health
curl http://localhost:9901/clusters

# View statistics
curl http://localhost:9901/stats

# Control plane status
curl http://localhost:8080/status

# Container logs
docker-compose logs envoy-proxy-1
docker-compose logs control-plane
```

## Best Practices

1. **Always use health checks** for all services
2. **Monitor metrics** continuously
3. **Version configurations** for rollback
4. **Test failover** scenarios regularly
5. **Document** custom configurations
6. **Use structured logging** for debugging
7. **Implement** circuit breakers and retries
8. **Secure** admin interfaces
9. **Plan** for gradual rollouts
10. **Automate** configuration management

## Future Enhancements

1. **Service Mesh Integration**:
   - Full Istio/Linkerd support
   - Mutual TLS between services

2. **Advanced Routing**:
   - Canary deployments
   - A/B testing
   - Traffic shadowing

3. **Enhanced Observability**:
   - Distributed tracing (Jaeger, Zipkin)
   - Metrics export (Prometheus)
   - Log aggregation (ELK stack)

4. **Security**:
   - WAF integration
   - DDoS protection
   - Rate limiting per user

5. **Multi-Region**:
   - Global load balancing
   - Geo-routing
   - Cross-region failover

## References

- [Envoy Documentation](https://www.envoyproxy.io/docs)
- [xDS Protocol](https://www.envoyproxy.io/docs/envoy/latest/api-docs/xds_protocol)
- [Service Mesh Patterns](https://www.envoyproxy.io/docs/envoy/latest/intro/what_is_envoy)
- [Docker Compose](https://docs.docker.com/compose/)

---

This architecture provides a robust, scalable, and production-ready API gateway solution!

# Service Mesh Implementation Guide

## Overview

This document provides detailed implementation details of the service mesh using Envoy Proxy and Rust microservices.

## Implementation Architecture

### Component Breakdown

```mermaid
graph TB
    subgraph "External Layer"
        C[Client]
    end

    subgraph "Ingress Layer"
        GE[Gateway Envoy<br/>Port 10000]
    end

    subgraph "Application Layer"
        GW[Gateway Service<br/>Rust - Port 8080]
    end

    subgraph "Service Layer"
        subgraph "User Service Pod"
            UE[User Envoy<br/>Port 15001]
            US[User Service<br/>Rust - Port 8081]
        end

        subgraph "Product Service Pod"
            PE[Product Envoy<br/>Port 15002]
            PS[Product Service<br/>Rust - Port 8082]
        end
    end

    subgraph "Observability Layer"
        PROM[Prometheus<br/>Port 9090]
        GRAF[Grafana<br/>Port 3000]
    end

    C -->|HTTP| GE
    GE -->|Proxy| GW
    GW -->|HTTP| UE
    GW -->|HTTP| PE
    UE -->|Local| US
    PE -->|Local| PS

    GE -.->|Metrics| PROM
    UE -.->|Metrics| PROM
    PE -.->|Metrics| PROM
    PROM -->|Data| GRAF

    style GE fill:#FF6B6B
    style UE fill:#4ECDC4
    style PE fill:#4ECDC4
    style GW fill:#45B7D1
    style US fill:#96CEB4
    style PS fill:#96CEB4
```

## Request Flow

### Complete Request Path

```mermaid
sequenceDiagram
    participant C as Client
    participant GE as Gateway Envoy<br/>(10000)
    participant GW as Gateway Service<br/>(8080)
    participant UE as User Service Envoy<br/>(15001)
    participant US as User Service<br/>(8081)
    participant PROM as Prometheus

    C->>GE: GET /api/users
    Note over GE: Route matching<br/>/api/users → user_service cluster

    GE->>GE: Load balance selection
    GE->>UE: HTTP GET /api/users
    Note over GE,PROM: Log request metrics

    UE->>UE: Route to local service
    UE->>US: HTTP GET /users
    Note over UE,PROM: Log request metrics

    US->>US: Process request<br/>Fetch from in-memory store
    US->>UE: 200 OK + JSON data

    UE->>UE: Record latency
    UE->>GE: 200 OK + JSON data

    GE->>GE: Record latency
    GE->>C: 200 OK + JSON data

    GE-.>>PROM: Push metrics
    UE-.>>PROM: Push metrics
```

### Path-Based Routing Flow

```mermaid
graph TB
    REQ[Client Request] --> GE[Gateway Envoy]

    GE --> ROUTE{Route Matcher}

    ROUTE -->|/api/users*| UC[User Service Cluster]
    ROUTE -->|/api/products*| PC[Product Service Cluster]
    ROUTE -->|/health| GC[Gateway Cluster]
    ROUTE -->|/*| GC

    UC --> UE[User Service Envoy]
    PC --> PE[Product Service Envoy]
    GC --> GW[Gateway Service]

    UE --> US[User Service]
    PE --> PS[Product Service]

    style ROUTE fill:#FFD700
```

## Envoy Configuration Deep Dive

### 1. Gateway Envoy Configuration

**Purpose**: Acts as ingress gateway, routing external traffic to internal services.

**Key Configuration Sections**:

```yaml
# Listener Configuration
listeners:
  - name: listener_0
    address:
      socket_address:
        address: 0.0.0.0
        port_value: 10000    # External ingress port
```

**Routing Logic**:

```yaml
routes:
  - match:
      prefix: "/api/users"    # Match user requests
    route:
      cluster: user_service   # Route to user service cluster
      timeout: 30s           # Request timeout

  - match:
      prefix: "/api/products" # Match product requests
    route:
      cluster: product_service # Route to product service cluster
      timeout: 30s
```

**Service Discovery**:

```yaml
clusters:
  - name: user_service
    type: STRICT_DNS           # DNS-based discovery
    dns_lookup_family: V4_ONLY
    lb_policy: ROUND_ROBIN     # Load balancing algorithm
    load_assignment:
      endpoints:
        - lb_endpoints:
          - endpoint:
              address:
                socket_address:
                  address: user-service-envoy  # Docker service name
                  port_value: 15001
```

### 2. Sidecar Envoy Configuration

**Purpose**: Proxy all traffic to/from the local service instance.

**Listener Setup**:

```yaml
listeners:
  - address:
      socket_address:
        address: 0.0.0.0
        port_value: 15001    # External-facing port
```

**Local Service Routing**:

```yaml
clusters:
  - name: local_user_service
    type: STATIC              # Static configuration for localhost
    load_assignment:
      endpoints:
        - lb_endpoints:
          - endpoint:
              address:
                socket_address:
                  address: 127.0.0.1  # Localhost
                  port_value: 8081     # Service port
```

### 3. Health Checking Configuration

**Active Health Checks**:

```yaml
health_checks:
  - timeout: 5s
    interval: 10s                    # Check every 10 seconds
    unhealthy_threshold: 2           # 2 failures = unhealthy
    healthy_threshold: 2             # 2 successes = healthy
    http_health_check:
      path: /health                  # Health endpoint
```

**Health Check State Machine**:

```mermaid
stateDiagram-v2
    [*] --> Healthy: Initial State
    Healthy --> Unhealthy: 2 consecutive failures
    Unhealthy --> Healthy: 2 consecutive successes
    Healthy --> Healthy: Success
    Unhealthy --> Unhealthy: Failure

    note right of Healthy
        Endpoint receives traffic
        Health check every 10s
    end note

    note right of Unhealthy
        Endpoint removed from load balancing
        Health check continues
    end note
```

## Rust Service Implementation

### Service Structure

All services follow a consistent structure:

```rust
// 1. Data structures with Serde for JSON serialization
#[derive(Serialize, Deserialize, Clone)]
struct Entity {
    id: String,
    // ... other fields
}

// 2. Application state (in-memory storage)
struct AppState {
    entities: Mutex<Vec<Entity>>,
}

// 3. HTTP handlers using Actix-web
async fn get_entities(data: web::Data<AppState>) -> impl Responder {
    // Handler logic
}

// 4. Main function with server setup
#[actix_web::main]
async fn main() -> std::io::Result<()> {
    // Initialize logging
    // Create application state
    // Configure routes
    // Start HTTP server
}
```

### Gateway Service Implementation

**Purpose**: Route requests to downstream services

**Key Features**:
- Service discovery via environment variables
- HTTP client for calling downstream services
- Error handling and graceful degradation
- Request logging

```rust
// Service URL from environment
let user_service_url = env::var("USER_SERVICE_URL")
    .unwrap_or_else(|_| "http://localhost:8081".to_string());

// Call downstream service
match reqwest::get(&format!("{}/users", user_service_url)).await {
    Ok(response) => {
        // Process response
    }
    Err(e) => {
        // Handle error - return 503 Service Unavailable
    }
}
```

### User/Product Service Implementation

**Purpose**: Handle domain-specific business logic

**Key Features**:
- In-memory data storage with Mutex for thread safety
- CRUD operations
- Health check endpoint
- Logging

```rust
// Thread-safe in-memory storage
struct AppState {
    users: Mutex<Vec<User>>,
}

// GET handler
async fn get_users(data: web::Data<AppState>) -> impl Responder {
    let users = data.users.lock().unwrap();
    HttpResponse::Ok().json(users.clone())
}

// GET by ID handler
async fn get_user(path: web::Path<String>, data: web::Data<AppState>) -> impl Responder {
    let user_id = path.into_inner();
    let users = data.users.lock().unwrap();

    match users.iter().find(|u| u.user_id == user_id) {
        Some(user) => HttpResponse::Ok().json(user.clone()),
        None => HttpResponse::NotFound().json(/* error */)
    }
}
```

## Docker Implementation

### Multi-Stage Build

All Rust services use multi-stage builds for optimal image size:

```dockerfile
# Stage 1: Build
FROM rust:1.87-slim AS builder
WORKDIR /app
COPY Cargo.toml ./
COPY src ./src
RUN cargo build --release

# Stage 2: Runtime
FROM debian:bookworm-slim
WORKDIR /app
COPY --from=builder /app/target/release/service-name /app/
CMD ["/app/service-name"]
```

**Benefits**:
- Small final image size (~100MB vs ~2GB)
- Only runtime dependencies in final image
- Faster deployment and scaling
- Better security (fewer attack surfaces)

### Docker Compose Networking

```yaml
networks:
  service-mesh:
    driver: bridge
```

**Network Features**:
- All containers on same network
- DNS resolution by container name
- Isolated from host network
- Inter-container communication

### Service Dependencies

```yaml
services:
  gateway:
    depends_on:
      - user-service
      - product-service
```

**Dependency Graph**:

```mermaid
graph TB
    GE[Gateway Envoy] --> GW[Gateway]
    GE --> UE[User Service Envoy]
    GE --> PE[Product Service Envoy]

    GW --> US[User Service]
    GW --> PS[Product Service]

    UE --> US
    PE --> PS

    PROM[Prometheus] --> GE
    PROM --> UE
    PROM --> PE

    GRAF[Grafana] --> PROM
```

## Observability Implementation

### Metrics Collection

**Envoy Metrics Endpoints**:

Each Envoy proxy exposes metrics at:
- Admin interface: `http://localhost:990X/stats/prometheus`
- Format: Prometheus exposition format

**Key Metric Categories**:

1. **Cluster Metrics**:
   - `envoy_cluster_upstream_rq_total`: Total requests to cluster
   - `envoy_cluster_upstream_rq_time`: Request duration histogram
   - `envoy_cluster_upstream_cx_active`: Active connections

2. **Listener Metrics**:
   - `envoy_listener_downstream_cx_total`: Total downstream connections
   - `envoy_listener_downstream_cx_active`: Active downstream connections

3. **HTTP Metrics**:
   - `envoy_http_downstream_rq_xx`: Response codes (2xx, 3xx, 4xx, 5xx)
   - `envoy_http_downstream_rq_time`: Request duration

### Prometheus Configuration

```yaml
scrape_configs:
  - job_name: 'gateway-envoy'
    static_configs:
      - targets: ['gateway-envoy:9901']
```

**Scrape Flow**:

```mermaid
sequenceDiagram
    participant P as Prometheus
    participant GE as Gateway Envoy<br/>(9901)
    participant UE as User Envoy<br/>(9902)
    participant PE as Product Envoy<br/>(9903)

    loop Every 15 seconds
        P->>GE: GET /stats/prometheus
        GE->>P: Metrics data

        P->>UE: GET /stats/prometheus
        UE->>P: Metrics data

        P->>PE: GET /stats/prometheus
        PE->>P: Metrics data
    end

    Note over P: Store metrics<br/>in time-series DB
```

### Access Logging

**Log Format**:

```
[timestamp] "method path protocol" status duration bytes_sent bytes_received "upstream_cluster"
```

**Example Log Entry**:

```
[2025-01-15T10:30:45.123Z] "GET /api/users HTTP/1.1" 200 1245 0 234 "user_service"
```

**What Each Field Means**:
- Method: HTTP verb (GET, POST, etc.)
- Path: Request path
- Protocol: HTTP version
- Status: Response code
- Duration: Request duration in milliseconds
- Bytes sent: Response size
- Bytes received: Request size
- Upstream cluster: Backend service that handled request

## Service Mesh Features

### 1. Load Balancing

**Algorithm**: Round Robin

```mermaid
graph TB
    REQ[Request] --> LB[Load Balancer]

    LB -->|Request 1| E1[Endpoint 1]
    LB -->|Request 2| E2[Endpoint 2]
    LB -->|Request 3| E3[Endpoint 3]
    LB -->|Request 4| E1

    style LB fill:#FFD700
```

**Configuration**:

```yaml
lb_policy: ROUND_ROBIN
```

**Distribution**:
- Requests evenly distributed across healthy endpoints
- No sticky sessions
- Automatic rebalancing on endpoint changes

### 2. Service Discovery

**Type**: DNS-based discovery

```mermaid
graph LR
    ENV[Envoy] -->|DNS Query| DNS[Docker DNS]
    DNS -->|IP Address| ENV
    ENV -->|HTTP Request| SVC[Service Instance]
```

**How it works**:
1. Envoy queries Docker's internal DNS
2. DNS returns IP of container(s) with matching service name
3. Envoy maintains connection pool to discovered endpoints
4. Automatic updates when services scale

### 3. Health Checking

**Check Flow**:

```mermaid
sequenceDiagram
    participant E as Envoy
    participant S as Service

    loop Every 10 seconds
        E->>S: GET /health
        alt Service Healthy
            S->>E: 200 OK
            Note over E: Mark as healthy<br/>Include in load balancing
        else Service Unhealthy
            S->>E: 500 Error / Timeout
            Note over E: Increment failure count<br/>After 2 failures, mark unhealthy
        end
    end
```

**Impact on Traffic**:
- Healthy endpoints receive traffic
- Unhealthy endpoints excluded from load balancing
- Continuous health checking even when unhealthy
- Automatic recovery when health restored

### 4. Timeout Management

**Configuration**:

```yaml
route:
  cluster: service_name
  timeout: 30s    # Request timeout
```

**Timeout Hierarchy**:

```mermaid
graph TB
    REQ[Request] --> GE[Gateway Envoy<br/>30s timeout]
    GE --> SE[Sidecar Envoy<br/>No timeout]
    SE --> SVC[Service<br/>Processing]

    SVC -.->|After 30s| TIMEOUT[Timeout Response<br/>504 Gateway Timeout]

    style TIMEOUT fill:#FF6B6B
```

### 5. Circuit Breaking

**Health-Based Circuit Breaking**:

Envoy removes unhealthy endpoints from load balancing pool:

```mermaid
stateDiagram-v2
    [*] --> Healthy
    Healthy --> Degraded: 1 failure
    Degraded --> Unhealthy: 2nd failure
    Unhealthy --> Degraded: Health check passes
    Degraded --> Healthy: 2nd success

    note right of Unhealthy
        Removed from load balancing
        Traffic routed to healthy endpoints
    end note
```

## Performance Characteristics

### Latency Impact

**Baseline (No Proxy)**:
- Direct service-to-service: ~1-2ms

**With Envoy Proxies**:
- Gateway Envoy overhead: ~1-2ms
- Sidecar Envoy overhead: ~1-2ms per hop
- Total additional latency: ~2-4ms

**Latency Breakdown**:

```mermaid
graph LR
    C[Client] -->|0ms| GE[Gateway Envoy<br/>+1ms]
    GE -->|Network| GW[Gateway Service<br/>+5ms processing]
    GW -->|Network| UE[User Envoy<br/>+1ms]
    UE -->|0ms| US[User Service<br/>+10ms processing]

    US -->|0ms| UE
    UE -->|Network| GW
    GW -->|Network| GE
    GE -->|0ms| C

    style GE fill:#FFD700
    style UE fill:#FFD700
```

**Total Request Time**: ~17-20ms typical

### Resource Usage

**Per Envoy Proxy**:
- Memory: 50-100MB (idle)
- CPU: 0.1-0.5 cores (under load)

**Per Rust Service**:
- Memory: 10-20MB
- CPU: 0.1-0.3 cores (under load)

## Security Considerations

### Current Implementation

 **Implemented**:
- Network isolation via Docker networks
- Container isolation
- No root user in containers
- Minimal base images

 **Not Implemented** (Future Enhancement):
- mTLS between services
- JWT authentication
- Rate limiting
- IP allowlisting

### Adding Security

**Step 1: Generate Certificates**

```bash
# Generate CA
openssl genrsa -out ca-key.pem 2048
openssl req -new -x509 -days 365 -key ca-key.pem -out ca.pem

# Generate service certificates
openssl genrsa -out service-key.pem 2048
openssl req -new -key service-key.pem -out service.csr
openssl x509 -req -days 365 -in service.csr -CA ca.pem -CAkey ca-key.pem -out service-cert.pem
```

**Step 2: Update Envoy Configuration**

```yaml
transport_socket:
  name: envoy.transport_sockets.tls
  typed_config:
    "@type": type.googleapis.com/envoy.extensions.transport_sockets.tls.v3.DownstreamTlsContext
    common_tls_context:
      tls_certificates:
      - certificate_chain: {filename: /etc/ssl/certs/service-cert.pem}
        private_key: {filename: /etc/ssl/certs/service-key.pem}
      validation_context:
        trusted_ca: {filename: /etc/ssl/certs/ca.pem}
```

## Scalability

### Horizontal Scaling

**Scale a Service**:

```bash
docker compose up -d --scale user-service=3
```

**What Happens**:

```mermaid
graph TB
    ENV[Envoy Proxy] -->|Round Robin| US1[User Service 1]
    ENV -->|Round Robin| US2[User Service 2]
    ENV -->|Round Robin| US3[User Service 3]

    style ENV fill:#4ECDC4
```

**Automatic**:
- DNS returns all service IPs
- Envoy discovers all instances
- Load balancing across all instances
- Health checking for each instance

### Vertical Scaling

**Resource Limits in Docker Compose**:

```yaml
services:
  user-service:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 1G
        reservations:
          cpus: '1'
          memory: 512M
```

## Troubleshooting Guide

### Common Issues

**1. Services Not Communicating**

Check:
```bash
# Verify containers are on same network
docker network inspect service-mesh_service-mesh

# Test connectivity
docker compose exec gateway ping user-service-envoy
```

**2. High Error Rates**

Check:
```bash
# View Envoy stats
curl http://localhost:9901/stats | grep upstream_rq

# Check health status
curl http://localhost:9901/clusters
```

**3. Metrics Not Appearing**

Check:
```bash
# Verify Prometheus targets
curl http://localhost:9090/api/v1/targets

# Check Envoy admin interface
curl http://localhost:9901/stats/prometheus
```

## Best Practices Demonstrated

1. **Separation of Concerns**: Proxies handle cross-cutting concerns
2. **Health Checks**: All services implement health endpoints
3. **Observability**: Comprehensive metrics and logging
4. **Resource Limits**: Defined in Dockerfiles
5. **Configuration as Code**: All config in version control
6. **Immutable Infrastructure**: Container-based deployment

## Next Steps

1. **Add mTLS**: Secure inter-service communication
2. **Implement Rate Limiting**: Protect services from overload
3. **Add Distributed Tracing**: Full request tracing with Jaeger
4. **Implement Circuit Breaking**: Advanced failure handling
5. **Deploy to Kubernetes**: Production-ready orchestration
6. **Add Control Plane**: Integrate Istio or Consul

---

This implementation serves as a foundation for understanding service mesh concepts and can be extended with additional features as needed.

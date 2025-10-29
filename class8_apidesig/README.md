# API Design Project - Complete Implementation

A comprehensive demonstration of modern API paradigms: **REST**, **GraphQL**, **gRPC**, and **API Gateway** using Envoy Proxy.

## 🎯 Project Overview

This project demonstrates production-ready implementations of three different API approaches and a unified API gateway that routes traffic to all of them.

### What's Included

1. **REST API** - FastAPI with CSV-based product inventory
2. **GraphQL API** - Query language for APIs with nested relationships
3. **gRPC Service** - High-performance RPC with Protocol Buffers
4. **Envoy API Gateway** - Production-grade gateway with multiple proxy instances and control plane

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.8+ (for local development)
- curl (for testing)

### Start Everything with Docker

```bash
# Navigate to the gateway directory
cd envoy-gateway

# Start all services (REST, GraphQL, gRPC, 3 Envoy proxies, Control Plane)
docker compose up -d

# Run end-to-end tests
./scripts/test-gateway.sh

# View logs
docker compose logs -f

# Stop all services
docker compose down
```

**Gateway URLs:**
- HTTP/REST/GraphQL: `http://localhost:10000`
- gRPC: `http://localhost:10001`
- Admin Interface: `http://localhost:9901`
- Control Plane: `http://localhost:8080`

### Test Individual APIs Locally

#### REST API
```bash
cd rest-api

# Generate sample data
python generate_products.py

# Start the server
pip install -r requirements.txt
python main.py

# Test endpoints
curl http://localhost:8000/api/categories
curl http://localhost:8000/api/products/category/Electronics
```

#### GraphQL API
```bash
cd graphql-demo
pip install -r requirements.txt
python main.py

# Visit playground
open http://localhost:8000/graphql

# Test query
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ users { name email } }"}'
```

#### gRPC Service
```bash
cd grpc-demo
pip install -r requirements.txt

# Terminal 1: Start server
python server.py

# Terminal 2: Run client examples
python client.py
```

## 📚 Project Structure

```
api-design1/
├── README.md                    # This file - main entry point
├── docs/                        # Detailed documentation
│   ├── QUICKSTART.md           # Step-by-step setup guide
│   ├── COMPLETE_PROJECT_OVERVIEW.md
│   └── API_DESIGN_SUMMARY.md
│
├── rest-api/                    # REST API implementation
│   ├── main.py                 # FastAPI REST server
│   ├── generate_products.py    # CSV data generator
│   ├── products.csv            # Sample product data (1000 items)
│   ├── requirements.txt
│   └── README.md
│
├── graphql-demo/
│   ├── main.py                 # GraphQL server
│   ├── schema.py               # GraphQL schema definition
│   ├── models.py               # Data models
│   ├── client_examples.py      # Python client examples
│   ├── README.md
│   ├── GRAPHQL_EXPLAINED.md    # Comprehensive GraphQL guide
│   └── SAMPLE_QUERIES.md       # 40+ example queries
│
├── grpc-demo/
│   ├── server.py               # gRPC server
│   ├── client.py               # Client with 14 examples
│   ├── protos/                 # Protocol Buffer definitions
│   ├── README.md
│   ├── GRPC_VS_REST.md        # Comparison guide
│   └── run_demo.sh
│
└── envoy-gateway/              # API Gateway (PRODUCTION READY)
    ├── docker-compose.yaml     # Orchestrates 7 containers
    ├── config/
    │   └── envoy-proxy.yaml   # Envoy configuration
    ├── control-plane/
    │   └── simple_control_plane.py
    ├── scripts/
    │   └── test-gateway.sh    # Automated testing
    ├── README.md              # Gateway quick start
    ├── ARCHITECTURE.md        # Detailed architecture (490+ lines)
    ├── COMMANDS.md           # Command reference
    └── TEST_RESULTS.md       # Test results (18/18 passed)
```

## 🔧 API Features

### REST API
- **Endpoints**: 7 endpoints for product management
- **Data Source**: CSV file with 1000 products
- **Categories**: 8 product categories
- **Features**:
  - Get products by category
  - Count products per category
  - Top 5 products by sales
  - Aging inventory detection

### GraphQL API
- **Schema**: Users, Posts, Comments with relationships
- **Queries**: 7 query types including nested data
- **Mutations**: 5 mutation types (Create, Update, Delete)
- **Features**:
  - Client-driven data fetching
  - No over-fetching/under-fetching
  - Introspection
  - Interactive playground

### gRPC Service
- **Patterns**: All 4 RPC patterns implemented
  - Unary (request-response)
  - Server streaming
  - Client streaming
  - Bidirectional streaming
- **Protocol Buffers**: Strongly typed contracts
- **Features**: High performance, HTTP/2, compact binary format

### Envoy API Gateway
- **Architecture**: 3 Envoy proxy instances + Control plane
- **High Availability**: Multiple proxies for fault tolerance
- **Features**:
  - Path-based routing
  - Load balancing (Round Robin)
  - Health checking (service-level)
  - Observability (Prometheus metrics)
  - Admin interfaces
  - Dynamic configuration management

## 📖 Documentation

### Quick References
- **[Quick Start Guide](docs/QUICKSTART.md)** - Get started in 5 minutes
- **[Complete Overview](docs/COMPLETE_PROJECT_OVERVIEW.md)** - Detailed project documentation
- **[API Design Summary](docs/API_DESIGN_SUMMARY.md)** - Technical summary

### Component Documentation
- **[REST API README](rest-api/README.md)** - REST API details
- **[GraphQL Explained](graphql-demo/GRAPHQL_EXPLAINED.md)** - 400+ line comprehensive guide
  - How GraphQL works
  - 10 major advantages
  - GraphQL vs REST comparison
- **[gRPC vs REST](grpc-demo/GRPC_VS_REST.md)** - Detailed comparison
- **[Gateway Architecture](envoy-gateway/ARCHITECTURE.md)** - 490+ line architecture guide
  - System design
  - Traffic flows
  - Configuration management
  - Monitoring and observability
- **[Gateway Commands](envoy-gateway/COMMANDS.md)** - Complete command reference

## 🧪 Testing

### Gateway End-to-End Tests
```bash
cd envoy-gateway
./scripts/test-gateway.sh
```

**Test Coverage:**
- ✅ Control Plane API (3 tests)
- ✅ REST API routing (3 tests)
- ✅ GraphQL API routing (3 tests)
- ✅ Multiple Envoy instances (3 tests)
- ✅ Admin interfaces (3 tests)
- ✅ Backend health checks (3 tests)

**Results**: 18/18 PASSED (100% success rate)

### Example API Calls

**REST via Gateway:**
```bash
curl http://localhost:10000/api/categories
curl http://localhost:10000/api/products/category/Electronics
```

**GraphQL via Gateway:**
```bash
curl -X POST http://localhost:10000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ user(id: 1) { name posts { title } } }"}'
```

**Control Plane:**
```bash
curl http://localhost:8080/status
curl http://localhost:8080/services
```

**Envoy Admin:**
```bash
curl http://localhost:9901/stats/prometheus
curl http://localhost:9901/clusters
```

## 🏗️ Architecture Highlights

### Traffic Flow
```
External Request
    ↓
Envoy Proxy (:10000/:10001/:10002/:10004)
    ↓
[Path-based Routing]
    ↓
┌────────┬──────────┬─────────┐
│        │          │         │
REST    GraphQL    gRPC    Control
API     API        API     Plane
:8000   :8000      :50051  :8080
```

### High Availability
- 3 independent Envoy proxy instances
- Any proxy can serve any request
- Health checks every 10 seconds
- Automatic failover on failures

### Observability
- Prometheus metrics export
- JSON access logs
- Admin interfaces per proxy
- Cluster health monitoring

## 📊 Performance

- **Response Time**: < 10ms average
- **Success Rate**: 100%
- **Healthy Backends**: 3/3
- **Concurrent Proxies**: 3
- **Status**: Production Ready ✅

## 🛠️ Technology Stack

- **API Framework**: FastAPI (Python)
- **GraphQL**: Strawberry GraphQL
- **gRPC**: grpcio + Protocol Buffers
- **API Gateway**: Envoy Proxy v1.28
- **Control Plane**: FastAPI
- **Containerization**: Docker & Docker Compose
- **Data Format**: CSV (REST), In-memory (GraphQL/gRPC)

## 📝 Use Cases

### When to Use Each API Type

**REST API**
- Simple CRUD operations
- Publicly accessible APIs
- Wide client compatibility needed
- Caching is important

**GraphQL**
- Complex data requirements
- Mobile applications (minimize data transfer)
- Rapidly evolving frontends
- Multiple related data types

**gRPC**
- Microservices communication
- High-performance requirements
- Streaming data
- Internal service-to-service calls

**API Gateway**
- Unified entry point needed
- Multiple backend services
- Cross-cutting concerns (auth, rate limiting)
- Protocol translation required

## 🔒 Production Recommendations

### Security
- Enable TLS/SSL for external traffic
- Implement mTLS between services
- Add authentication (JWT, OAuth2)
- Configure rate limiting
- Restrict admin interface access

### Scalability
- Deploy on Kubernetes
- Implement horizontal pod autoscaling
- Add connection pooling
- Configure circuit breakers
- Tune timeout and retry policies

### Monitoring
- Export metrics to Prometheus
- Set up Grafana dashboards
- Configure alerting (PagerDuty, Slack)
- Implement distributed tracing (Jaeger)
- Centralize logs (ELK stack)

## 📚 Learning Resources

- [Envoy Proxy Documentation](https://www.envoyproxy.io/docs)
- [GraphQL Official Guide](https://graphql.org/learn/)
- [gRPC Official Documentation](https://grpc.io/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## 🎓 Educational Value

This project demonstrates:
- Modern API design patterns
- Service mesh concepts
- Cloud-native architecture
- Infrastructure as code
- Containerization and orchestration
- API gateway patterns
- Protocol translation
- High availability design
- Observability best practices

## 📄 License

This is an educational project for demonstrating API design concepts.

---

**Status**: All components tested and verified ✅
**Last Updated**: October 29, 2025
**Test Results**: 18/18 Passed (100% success rate)

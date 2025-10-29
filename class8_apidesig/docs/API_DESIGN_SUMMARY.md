# API Design Project - Complete Summary

This project demonstrates three different API paradigms: REST API using FastAPI, gRPC using Python, and GraphQL using FastAPI + Strawberry.

## Project Overview

```
api-design1/
├── FastAPI REST API Demo
│   ├── generate_products.py    # Generate sample CSV data
│   ├── products.csv            # 1000 product records
│   ├── main.py                 # FastAPI application
│   ├── requirements.txt        # FastAPI dependencies
│   └── README.md              # FastAPI documentation
│
├── gRPC Demo
│   ├── protos/
│   │   └── user_service.proto  # Service definition
│   ├── server.py               # gRPC server
│   ├── client.py               # gRPC client
│   ├── run_demo.sh            # Demo script
│   ├── requirements.txt        # gRPC dependencies
│   ├── README.md              # gRPC documentation
│   └── GRPC_VS_REST.md        # Comparison guide
│
└── GraphQL Demo
    ├── main.py                 # FastAPI + GraphQL server
    ├── schema.py               # GraphQL schema
    ├── models.py               # Data models
    ├── client_examples.py      # Python client examples
    ├── requirements.txt        # GraphQL dependencies
    ├── README.md              # GraphQL documentation
    ├── GRAPHQL_EXPLAINED.md   # Comprehensive guide
    └── SAMPLE_QUERIES.md      # Query examples
```

## Part 1: FastAPI REST API

### Overview
A REST API for managing product inventory with CSV data storage.

### Features
- Read product data from CSV file
- Get products by category
- Get product counts per category
- Get top products by sales
- Get aging inventory
- Pagination support

### Data Structure
Each product includes:
- product_id, name, category, price
- quantity_in_stock, sales
- last_stock_date, supplier

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/products/category/{category}` | Products by category |
| GET | `/products/category-counts` | Product count per category |
| GET | `/products/top-sales/{category}` | Top 5 by sales |
| GET | `/products/aging-inventory` | Top 5 aging inventory |
| GET | `/products/all` | All products (paginated) |
| GET | `/categories` | List all categories |

### Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Generate sample data (already done)
python generate_products.py

# Run the API
python main.py

# Access API at http://localhost:8000
# Interactive docs at http://localhost:8000/docs
```

### Sample Categories
Electronics, Clothing, Home & Kitchen, Sports, Books, Toys, Beauty, Automotive

### Sample Request

```bash
# Get products in Electronics category
curl http://localhost:8000/products/category/Electronics

# Get top 5 products by sales in Sports
curl http://localhost:8000/products/top-sales/Sports?limit=5

# Get aging inventory
curl http://localhost:8000/products/aging-inventory?limit=5
```

---

## Part 2: gRPC Python Demo

### Overview
Comprehensive demonstration of all four gRPC communication patterns.

### gRPC Patterns Demonstrated

1. **Unary RPC** (Request-Response)
   - GetUser: Get single user by ID
   - CreateUser: Create new user

2. **Server Streaming RPC**
   - ListUsers: Server streams multiple users

3. **Client Streaming RPC**
   - BatchCreateUsers: Client streams creation requests

4. **Bidirectional Streaming RPC**
   - StreamUsers: Chat-like messaging

### Service Definition

```protobuf
service UserService {
  rpc GetUser (GetUserRequest) returns (UserResponse) {}
  rpc CreateUser (CreateUserRequest) returns (UserResponse) {}
  rpc ListUsers (ListUsersRequest) returns (stream UserResponse) {}
  rpc BatchCreateUsers (stream CreateUserRequest) returns (BatchCreateResponse) {}
  rpc StreamUsers (stream UserMessage) returns (stream UserMessage) {}
}
```

### Quick Start

```bash
cd grpc-demo

# Option 1: Use the demo script (easiest)
./run_demo.sh

# Option 2: Manual
pip install -r requirements.txt

# Terminal 1: Start server
python server.py

# Terminal 2: Run client
python client.py
```

### What You'll See

The client automatically runs through all five demos:
1. ✅ Unary RPC: GetUser
2. ✅ Unary RPC: CreateUser
3. ✅ Server Streaming: ListUsers
4. ✅ Client Streaming: BatchCreateUsers
5. ✅ Bidirectional Streaming: StreamUsers

---

## Key Differences: REST vs gRPC

### REST API (FastAPI)
✅ **Pros:**
- Easy to understand
- Browser-friendly
- Human-readable JSON
- Wide tooling support
- Great for public APIs

❌ **Cons:**
- Larger payload sizes
- No native streaming
- Text-based parsing overhead
- Limited type safety

### gRPC
✅ **Pros:**
- High performance (binary)
- Native streaming (4 types)
- Strong typing
- Auto code generation
- Efficient for microservices

❌ **Cons:**
- Steeper learning curve
- Limited browser support
- Binary format (not human-readable)
- Requires .proto definitions

### Performance Comparison

| Metric | REST (JSON) | gRPC (Protobuf) |
|--------|-------------|-----------------|
| Payload Size | 100 KB | ~40 KB (60% smaller) |
| Serialization | Slower | Faster |
| Streaming | Limited | Native |
| Type Safety | Low | High |
| Browser Support | Full | Limited |

---

## When to Use What?

### Use REST API when:
- Building public-facing APIs
- Browser compatibility is critical
- Simple CRUD operations
- Human readability matters
- Quick prototyping needed

**Example Use Cases:**
- E-commerce product APIs
- Content management systems
- Public web services
- Mobile app backends (simple)

### Use gRPC when:
- Building microservices
- Performance is critical
- Real-time streaming needed
- Internal service communication
- Strong typing required

**Example Use Cases:**
- Microservice architectures
- Real-time chat applications
- IoT device communication
- High-frequency trading systems
- Live video streaming

---

## Learning Objectives Achieved

### REST API Concepts
✅ RESTful design principles
✅ HTTP methods (GET)
✅ JSON serialization
✅ Query parameters
✅ Path parameters
✅ Pagination
✅ Status codes
✅ OpenAPI/Swagger documentation

### gRPC Concepts
✅ Protocol Buffers
✅ Service definitions
✅ Unary RPCs
✅ Server streaming
✅ Client streaming
✅ Bidirectional streaming
✅ Code generation
✅ HTTP/2 transport
✅ Error handling with status codes

### Python Concepts
✅ FastAPI framework
✅ gRPC Python libraries
✅ Async/await patterns
✅ Generator functions
✅ CSV file handling
✅ Pydantic models
✅ Type hints

---

## Testing the APIs

### Test FastAPI REST API

```bash
# Using curl
curl http://localhost:8000/categories
curl http://localhost:8000/products/category/Electronics
curl http://localhost:8000/products/category-counts

# Using Python requests
import requests
response = requests.get('http://localhost:8000/categories')
print(response.json())

# Using browser
# Visit http://localhost:8000/docs for interactive API docs
```

### Test gRPC API

```bash
# Using the provided client
python grpc-demo/client.py

# Using grpcurl (if installed)
grpcurl -plaintext localhost:50051 list
grpcurl -plaintext localhost:50051 describe user.UserService

# Using BloomRPC or Postman (GUI tools)
```

---

## Advanced Topics

### For REST API
- Add authentication (JWT)
- Implement POST/PUT/DELETE
- Add database (PostgreSQL, MongoDB)
- Rate limiting
- Caching with Redis
- CORS configuration
- Docker deployment

### For gRPC
- Add TLS/SSL encryption
- Implement authentication (tokens)
- Add interceptors (middleware)
- Load balancing
- Service discovery
- Observability (metrics, tracing)
- gRPC-Gateway (REST bridge)

---

## Resources

### FastAPI
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [OpenAPI Specification](https://swagger.io/specification/)

### gRPC
- [gRPC Official Documentation](https://grpc.io/docs/)
- [Protocol Buffers Guide](https://protobuf.dev/)
- [gRPC Python Tutorial](https://grpc.io/docs/languages/python/)
- [HTTP/2 Explained](https://http2.github.io/)

### API Design
- [REST API Best Practices](https://restfulapi.net/)
- [API Design Patterns](https://www.apiopscycles.com/)
- [Microservices Patterns](https://microservices.io/patterns/)

---

## Part 3: GraphQL Demo

### Overview
A comprehensive GraphQL implementation with FastAPI and Strawberry GraphQL.

### Features
- Complete GraphQL schema (Types, Queries, Mutations)
- Relationships (Users → Posts → Comments)
- Computed fields with logic
- Field arguments
- Variables and aliases
- Search and filtering
- Interactive GraphQL Playground

### Data Models
- **User**: username, email, name, age, city
- **Post**: title, content, author, likes, published
- **Comment**: text, author, post

### Queries

| Query | Description |
|-------|-------------|
| `hello` | Simple hello query |
| `user(id)` | Get single user |
| `users(limit)` | Get all users |
| `post(id)` | Get single post |
| `posts(publishedOnly)` | Get all posts |
| `searchPosts(keyword)` | Search posts |
| `popularPosts(minLikes)` | Get popular posts |

### Mutations

| Mutation | Description |
|----------|-------------|
| `createUser` | Create new user |
| `createPost` | Create new post |
| `createComment` | Create comment |
| `updatePost` | Update post |
| `deletePost` | Delete post |

### Quick Start

```bash
cd graphql-demo

# Install dependencies
pip install -r requirements.txt

# Run server
python main.py

# Access GraphQL Playground
# Open browser: http://localhost:8000/graphql
```

### Sample Query

```graphql
query {
  user(id: 1) {
    name
    email
    posts {
      title
      comments {
        text
        author {
          name
        }
      }
    }
  }
}
```

### Sample Mutation

```graphql
mutation {
  createPost(input: {
    title: "My Post"
    content: "Content here"
    authorId: 1
    published: true
  }) {
    id
    title
    author {
      name
    }
  }
}
```

### GraphQL Advantages Demonstrated

1. **No Over-fetching**: Request only needed fields
2. **No Under-fetching**: Get related data in one request
3. **Strong Typing**: Schema validation
4. **Self-Documentation**: Introspective schema
5. **Flexible Queries**: Client controls response shape
6. **Single Endpoint**: `/graphql` for all operations
7. **Nested Relationships**: Deep querying support
8. **Computed Fields**: `postCount`, `commentCount`
9. **Field Arguments**: `excerpt(length: 50)`
10. **Variables**: Parameterized queries

---

## Comparison: REST vs gRPC vs GraphQL

| Feature | REST | gRPC | GraphQL |
|---------|------|------|---------|
| **Protocol** | HTTP/1.1 | HTTP/2 | HTTP/1.1+ |
| **Data Format** | JSON | Protobuf | JSON |
| **Endpoints** | Multiple | Single | Single |
| **Over-fetching** | Common | N/A | Eliminated |
| **Under-fetching** | Common | N/A | Eliminated |
| **Streaming** | Limited | Native | Subscriptions |
| **Type Safety** | Low | High | High |
| **Learning Curve** | Easy | Medium | Medium |
| **Browser Support** | Full | Limited | Full |
| **Caching** | Easy | Complex | Complex |
| **Best For** | Public APIs | Microservices | Flexible UIs |

### When to Use Each

**REST**:
- ✅ Simple CRUD operations
- ✅ Public APIs
- ✅ Wide client compatibility
- ✅ HTTP caching important

**gRPC**:
- ✅ Microservices communication
- ✅ High performance requirements
- ✅ Streaming needed
- ✅ Internal services

**GraphQL**:
- ✅ Complex, nested data
- ✅ Multiple client platforms
- ✅ Rapid frontend development
- ✅ Flexible data requirements

---

## Conclusion

This project provides hands-on experience with three modern API paradigms:

- **REST**: Best for public APIs, web services, and simple CRUD operations
- **gRPC**: Best for microservices, high-performance systems, and streaming
- **GraphQL**: Best for flexible UIs, complex data requirements, and multiple clients

In modern architectures, it's common to use multiple approaches:
- gRPC for internal service-to-service communication
- REST for external/public-facing APIs
- GraphQL as an API gateway aggregating multiple services

Understanding all three paradigms makes you a more versatile developer and helps you choose the right tool for each use case.

## Next Steps

1. Experiment with modifying the APIs
2. Add new endpoints/RPCs
3. Implement authentication
4. Add database integration
5. Deploy to production
6. Monitor and optimize performance
7. Implement error handling
8. Add comprehensive testing

Happy coding! 🚀

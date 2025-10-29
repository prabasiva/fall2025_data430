# gRPC vs REST: A Comparison

## Overview

This document compares gRPC and REST API architectures to help you understand when to use each.

## Quick Comparison Table

| Feature | gRPC | REST |
|---------|------|------|
| **Protocol** | HTTP/2 | HTTP/1.1 (or HTTP/2) |
| **Data Format** | Protocol Buffers (binary) | JSON (text) |
| **API Contract** | Strict (.proto files) | Flexible (OpenAPI optional) |
| **Streaming** | Native support (4 types) | Limited (SSE, WebSockets) |
| **Browser Support** | Limited (requires gRPC-Web) | Full native support |
| **Performance** | High (binary, multiplexing) | Lower (text-based) |
| **Code Generation** | Automatic from .proto | Manual or via OpenAPI |
| **Learning Curve** | Steeper | Gentler |
| **Human Readable** | No (binary) | Yes (JSON) |
| **Payload Size** | Smaller | Larger |

## Detailed Comparison

### 1. Communication Pattern

**REST:**
- Request-Response only
- Client initiates all communication
- Polling required for real-time updates

```http
GET /api/users/1 HTTP/1.1
Host: example.com

HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 1,
  "name": "Alice Johnson",
  "email": "alice@example.com"
}
```

**gRPC:**
- Four communication patterns:
  1. Unary (request-response)
  2. Server streaming
  3. Client streaming
  4. Bidirectional streaming

```protobuf
service UserService {
  rpc GetUser (GetUserRequest) returns (UserResponse) {}
  rpc ListUsers (Empty) returns (stream UserResponse) {}
  rpc BatchCreate (stream CreateRequest) returns (BatchResponse) {}
  rpc Chat (stream Message) returns (stream Message) {}
}
```

### 2. Data Format

**REST (JSON):**
```json
{
  "user_id": 1,
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "age": 28,
  "created_at": "2025-10-29T10:00:00Z"
}
```
- Human-readable
- Larger payload size
- Flexible schema
- Slower parsing

**gRPC (Protocol Buffers):**
```protobuf
message UserResponse {
  int32 user_id = 1;
  string name = 2;
  string email = 3;
  int32 age = 4;
  string created_at = 5;
}
```
- Binary format
- 30-40% smaller payloads
- Strict schema
- Faster serialization/deserialization

### 3. Performance Comparison

#### Payload Size Example

For 1000 users:
- **REST (JSON)**: ~150 KB
- **gRPC (Protobuf)**: ~50 KB
- **Savings**: 66% reduction

#### Latency

- **REST**:
  - HTTP/1.1 connection per request
  - Text parsing overhead
  - No multiplexing

- **gRPC**:
  - Single HTTP/2 connection
  - Binary parsing (faster)
  - Request multiplexing
  - Header compression

**Result**: gRPC typically 2-10x faster depending on use case

### 4. API Design

**REST:**
```
GET    /api/users           # List users
GET    /api/users/1         # Get user
POST   /api/users           # Create user
PUT    /api/users/1         # Update user
DELETE /api/users/1         # Delete user
```
- Resource-oriented
- Uses HTTP verbs
- URL-based routing
- Stateless

**gRPC:**
```protobuf
service UserService {
  rpc ListUsers(ListRequest) returns (stream User) {}
  rpc GetUser(GetRequest) returns (User) {}
  rpc CreateUser(User) returns (User) {}
  rpc UpdateUser(User) returns (User) {}
  rpc DeleteUser(DeleteRequest) returns (Empty) {}
}
```
- RPC-oriented
- Method calls
- Strong typing
- Contract-first design

### 5. Code Generation

**REST:**
- Manual client implementation
- OR use OpenAPI/Swagger for generation
- Less type safety
- More boilerplate

**gRPC:**
- Automatic client/server generation
- Type-safe code
- Multiple language support
- Minimal boilerplate

### 6. Streaming Capabilities

**REST:**
- Server-Sent Events (SSE) for server push
- WebSockets for bidirectional
- Not built into HTTP/1.1
- Requires additional setup

**gRPC:**
- Native streaming support
- Four patterns built-in
- Efficient over single connection
- Part of HTTP/2 protocol

### 7. Error Handling

**REST (HTTP Status Codes):**
```http
200 OK
201 Created
400 Bad Request
401 Unauthorized
404 Not Found
500 Internal Server Error
```
- Well-understood
- Limited granularity
- Body for details

**gRPC (Status Codes):**
```
OK
CANCELLED
INVALID_ARGUMENT
NOT_FOUND
ALREADY_EXISTS
PERMISSION_DENIED
RESOURCE_EXHAUSTED
UNIMPLEMENTED
INTERNAL
UNAVAILABLE
```
- More specific error codes
- Rich error details
- Structured error messages

### 8. Browser Support

**REST:**
- ✅ Full native browser support
- ✅ Works with fetch/XMLHttpRequest
- ✅ CORS support
- ✅ No special tooling needed

**gRPC:**
- ⚠️ Limited native support
- ⚠️ Requires gRPC-Web proxy
- ⚠️ Additional complexity
- ❌ Not all features available

### 9. Use Cases

#### When to Use REST

✅ **Best for:**
- Public APIs (web browsers)
- Simple CRUD operations
- Human-readable requirements
- Quick prototyping
- Third-party integrations
- Wide client variety

**Examples:**
- Public web APIs
- Mobile app backends (simple)
- Content management systems
- E-commerce platforms
- Social media APIs

#### When to Use gRPC

✅ **Best for:**
- Microservices communication
- Real-time applications
- High-performance requirements
- Internal APIs
- IoT systems
- Mobile apps (complex)

**Examples:**
- Microservices architectures
- Real-time chat systems
- Live video streaming
- Gaming servers
- Financial trading systems
- IoT device communication

### 10. Example Implementations

#### REST Example (Python Flask)

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = get_user_from_db(user_id)
    return jsonify(user)

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    user = create_user_in_db(data)
    return jsonify(user), 201
```

#### gRPC Example (Python)

```python
import grpc
import user_service_pb2_grpc

class UserService(user_service_pb2_grpc.UserServiceServicer):
    def GetUser(self, request, context):
        user = get_user_from_db(request.user_id)
        return user_service_pb2.UserResponse(**user)

    def CreateUser(self, request, context):
        user = create_user_in_db(request)
        return user_service_pb2.UserResponse(**user)
```

### 11. Migration Strategy

If you're considering migrating from REST to gRPC:

1. **Start with internal services**
   - Less impact on external clients
   - Can iterate quickly

2. **Keep REST for public APIs**
   - Maintain browser compatibility
   - Don't break existing integrations

3. **Use both (Hybrid)**
   - gRPC for service-to-service
   - REST for web clients
   - Best of both worlds

4. **Use gRPC-Gateway**
   - Generate REST API from gRPC
   - Single source of truth
   - Supports both protocols

### 12. Tooling and Ecosystem

**REST:**
- Postman, Insomnia (testing)
- Swagger/OpenAPI (docs)
- cURL (command line)
- Extensive libraries

**gRPC:**
- BloomRPC, Postman (testing)
- grpcurl (command line)
- Built-in reflection
- Growing ecosystem

## Conclusion

**Choose REST when:**
- Building public-facing APIs
- Browser support is critical
- Human readability matters
- Simple CRUD operations
- Team familiarity is low

**Choose gRPC when:**
- Building microservices
- Performance is critical
- Streaming is needed
- Strong typing is important
- Internal communications

**Use Both when:**
- You have diverse clients
- Different performance needs
- Complex distributed system
- Want maximum flexibility

## Further Reading

- [gRPC Official Documentation](https://grpc.io/docs/)
- [REST API Best Practices](https://restfulapi.net/)
- [Protocol Buffers Guide](https://protobuf.dev/)
- [HTTP/2 Specification](https://http2.github.io/)

# gRPC Python Demo

A comprehensive demonstration of gRPC concepts in Python, showcasing all four types of RPC patterns.

## What is gRPC?

gRPC (gRPC Remote Procedure Call) is a high-performance, open-source framework developed by Google that enables efficient communication between distributed systems. It uses Protocol Buffers (protobuf) for serialization and HTTP/2 for transport.

### Key Features:
- **High Performance**: Binary serialization with Protocol Buffers
- **Language Agnostic**: Client and server can be written in different languages
- **Bi-directional Streaming**: Full-duplex communication
- **Built-in Authentication**: SSL/TLS and token-based authentication
- **Load Balancing**: Built-in support for load balancing

## RPC Patterns Demonstrated

This demo showcases all four gRPC communication patterns:

### 1. Unary RPC (Request-Response)
Simple request-response pattern, like traditional HTTP requests.

**Examples:**
- `GetUser`: Get a single user by ID
- `CreateUser`: Create a new user

### 2. Server Streaming RPC
Client sends one request, server sends back a stream of responses.

**Example:**
- `ListUsers`: Server streams multiple users to the client

### 3. Client Streaming RPC
Client sends a stream of requests, server sends back a single response.

**Example:**
- `BatchCreateUsers`: Client streams multiple user creation requests, server responds with summary

### 4. Bidirectional Streaming RPC
Both client and server send streams of messages independently.

**Example:**
- `StreamUsers`: Chat-like messaging where both sides stream messages

## Project Structure

```
grpc-demo/
├── protos/
│   └── user_service.proto      # Protocol Buffer definition
├── user_service_pb2.py          # Generated protobuf code
├── user_service_pb2_grpc.py     # Generated gRPC code
├── server.py                    # gRPC server implementation
├── client.py                    # gRPC client with demos
├── run_demo.sh                  # Script to run complete demo
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate gRPC Code (if needed)

The generated files are already included, but if you modify the `.proto` file, regenerate:

```bash
python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/user_service.proto
```

## Running the Demo

### Option 1: Using the Demo Script (Easiest)

```bash
./run_demo.sh
```

This script will:
1. Install dependencies if needed
2. Generate gRPC code if needed
3. Start the server
4. Run the client demos
5. Stop the server

### Option 2: Manual Setup

#### Start the Server

In one terminal:

```bash
python server.py
```

You should see:
```
gRPC Server started on port 50051
Server is ready to accept requests...
```

#### Run the Client

In another terminal:

```bash
python client.py
```

The client will run through all five demo scenarios automatically.

## Service Definition (Protocol Buffer)

```protobuf
service UserService {
  // Unary RPC
  rpc GetUser (GetUserRequest) returns (UserResponse) {}
  rpc CreateUser (CreateUserRequest) returns (UserResponse) {}

  // Server streaming RPC
  rpc ListUsers (ListUsersRequest) returns (stream UserResponse) {}

  // Client streaming RPC
  rpc BatchCreateUsers (stream CreateUserRequest) returns (BatchCreateResponse) {}

  // Bidirectional streaming RPC
  rpc StreamUsers (stream UserMessage) returns (stream UserMessage) {}
}
```

## API Examples

### 1. Get User (Unary RPC)

**Request:**
```python
stub.GetUser(user_service_pb2.GetUserRequest(user_id=1))
```

**Response:**
```python
UserResponse(
    user_id=1,
    name="Alice Johnson",
    email="alice@example.com",
    age=28,
    created_at="2025-10-29T10:00:00"
)
```

### 2. Create User (Unary RPC)

**Request:**
```python
stub.CreateUser(user_service_pb2.CreateUserRequest(
    name="John Doe",
    email="john.doe@example.com",
    age=32
))
```

### 3. List Users (Server Streaming)

**Request:**
```python
stub.ListUsers(user_service_pb2.ListUsersRequest(limit=3))
```

**Response:** Stream of UserResponse objects

### 4. Batch Create Users (Client Streaming)

**Request:** Stream of CreateUserRequest objects

**Response:**
```python
BatchCreateResponse(
    users_created=3,
    user_ids=[7, 8, 9]
)
```

### 5. Stream Users (Bidirectional Streaming)

Both client and server send streams of UserMessage objects.

## Key Concepts Demonstrated

### Protocol Buffers
- Efficient binary serialization
- Strong typing
- Backward/forward compatibility
- Cross-language support

### gRPC Features
- **Streaming**: Both client and server streaming
- **Error Handling**: gRPC status codes
- **Concurrency**: ThreadPoolExecutor for handling multiple requests
- **In-Memory Storage**: Simple user database simulation

### Python gRPC Components

1. **Server (`server.py`)**
   - Service implementation inheriting from generated servicer
   - ThreadPoolExecutor for concurrent request handling
   - Error handling with gRPC status codes

2. **Client (`client.py`)**
   - Channel creation and stub instantiation
   - Different patterns for each RPC type
   - Generator functions for streaming requests

3. **Proto Definition (`user_service.proto`)**
   - Service and RPC method definitions
   - Message type definitions
   - Field numbering for Protocol Buffers

## Testing Individual RPCs

You can also test individual RPCs by modifying `client.py` or creating custom scripts:

```python
import grpc
import user_service_pb2
import user_service_pb2_grpc

# Create channel
channel = grpc.insecure_channel('localhost:50051')
stub = user_service_pb2_grpc.UserServiceStub(channel)

# Get user
response = stub.GetUser(user_service_pb2.GetUserRequest(user_id=1))
print(f"User: {response.name}")
```

## Advantages of gRPC over REST

1. **Performance**: Binary protocol (protobuf) vs JSON
2. **Streaming**: Native support for streaming vs HTTP/1.1 limitations
3. **Type Safety**: Strong typing with Protocol Buffers
4. **Code Generation**: Automatic client/server code generation
5. **HTTP/2**: Multiplexing, server push, header compression

## Common Use Cases

- **Microservices**: Efficient inter-service communication
- **Real-time Applications**: Chat, notifications, live updates
- **IoT**: Low bandwidth, efficient communication
- **Mobile Apps**: Efficient mobile-backend communication
- **High-throughput Systems**: Financial trading, gaming

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 50051
lsof -i :50051

# Kill the process
kill -9 <PID>
```

### Module Not Found
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Proto Changes Not Reflected
```bash
# Regenerate gRPC code
python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/user_service.proto
```

## Further Learning

- [gRPC Official Documentation](https://grpc.io/docs/)
- [Protocol Buffers Documentation](https://protobuf.dev/)
- [gRPC Python Quickstart](https://grpc.io/docs/languages/python/quickstart/)
- [gRPC Best Practices](https://grpc.io/docs/guides/performance/)

## License

This is a demo project for educational purposes.

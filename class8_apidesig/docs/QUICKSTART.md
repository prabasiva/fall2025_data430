# Quick Start Guide

Get all three APIs up and running in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Option 1: FastAPI REST API

```bash
# 1. Install dependencies
pip install fastapi uvicorn pydantic

# 2. Run the API (data already generated)
python main.py

# 3. Test it
# Open browser: http://localhost:8000/docs
# Or use curl:
curl http://localhost:8000/categories
curl http://localhost:8000/products/category/Electronics
```

**That's it!** 🎉 Your REST API is running on port 8000.

### Available Endpoints:
- 📋 Interactive docs: http://localhost:8000/docs
- 🔍 Get categories: http://localhost:8000/categories
- 📦 Get products: http://localhost:8000/products/category/Electronics
- 📊 Category counts: http://localhost:8000/products/category-counts
- 🏆 Top sales: http://localhost:8000/products/top-sales/Sports
- ⏰ Aging inventory: http://localhost:8000/products/aging-inventory

---

## Option 2: gRPC Demo

```bash
# 1. Navigate to gRPC demo
cd grpc-demo

# 2. Run the complete demo
./run_demo.sh
```

**That's it!** 🎉 The script handles everything automatically.

### What It Does:
1. ✅ Installs dependencies (grpcio, grpcio-tools, protobuf)
2. ✅ Generates Python code from .proto file
3. ✅ Starts the gRPC server (port 50051)
4. ✅ Runs client demos (all 5 RPC patterns)
5. ✅ Stops the server

### Manual Mode (if you prefer):

```bash
# Terminal 1: Start server
cd grpc-demo
pip install -r requirements.txt
python server.py

# Terminal 2: Run client
cd grpc-demo
python client.py
```

---

## Quick Test Commands

### FastAPI REST API

```bash
# Get all categories
curl http://localhost:8000/categories

# Get products in a specific category
curl http://localhost:8000/products/category/Electronics

# Get top 5 products by sales in Sports
curl http://localhost:8000/products/top-sales/Sports?limit=5

# Get aging inventory
curl http://localhost:8000/products/aging-inventory

# Get product counts per category
curl http://localhost:8000/products/category-counts
```

### gRPC (using Python)

```python
import grpc
import user_service_pb2
import user_service_pb2_grpc

# Connect to server
channel = grpc.insecure_channel('localhost:50051')
stub = user_service_pb2_grpc.UserServiceStub(channel)

# Get user
response = stub.GetUser(user_service_pb2.GetUserRequest(user_id=1))
print(f"User: {response.name}")

# Create user
new_user = stub.CreateUser(user_service_pb2.CreateUserRequest(
    name="Test User",
    email="test@example.com",
    age=30
))
print(f"Created user with ID: {new_user.user_id}")
```

---

## Troubleshooting

### Port Already in Use

**FastAPI:**
```bash
# Kill process on port 8000
lsof -i :8000
kill -9 <PID>

# Or use different port
uvicorn main:app --port 8001
```

**gRPC:**
```bash
# Kill process on port 50051
lsof -i :50051
kill -9 <PID>
```

### Module Not Found

```bash
# For FastAPI
pip install fastapi uvicorn pydantic

# For gRPC
cd grpc-demo
pip install -r requirements.txt
```

### Permission Denied (run_demo.sh)

```bash
chmod +x grpc-demo/run_demo.sh
```

---

## Option 3: GraphQL

```bash
# 1. Navigate to GraphQL demo
cd graphql-demo

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the server
python main.py

# 4. Open GraphQL Playground
# Visit: http://localhost:8000/graphql
```

**That's it!** 🎉 Your GraphQL API is running with an interactive playground.

### Try These Queries:

**Simple Query:**
```graphql
query {
  hello
  users {
    name
    email
  }
}
```

**Nested Query:**
```graphql
query {
  user(id: 1) {
    name
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

**Mutation:**
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
  }
}
```

### Available Features:
- 🎮 Interactive GraphQL Playground
- 📊 7 queries, 5 mutations
- 🔗 Nested relationships
- 📝 40+ sample queries in SAMPLE_QUERIES.md
- 🐍 14 Python client examples
- 📖 400+ line comprehensive guide (GRAPHQL_EXPLAINED.md)

---

## What's Next?

1. **Explore the APIs**
   - Try different endpoints
   - Modify query parameters
   - Test error cases

2. **Read the Docs**
   - `README.md` - FastAPI REST documentation
   - `grpc-demo/README.md` - gRPC documentation
   - `graphql-demo/GRAPHQL_EXPLAINED.md` - **GraphQL comprehensive guide (400+ lines)**
   - `API_DESIGN_SUMMARY.md` - Complete overview
   - `COMPLETE_PROJECT_OVERVIEW.md` - Detailed project overview

3. **Experiment**
   - Modify the code
   - Add new endpoints
   - Create custom queries
   - Test performance

4. **Learn More**
   - Compare REST vs gRPC performance
   - Implement authentication
   - Add database integration
   - Deploy to production

---

## Quick Reference

### FastAPI REST API
- **Port**: 8000
- **Docs**: http://localhost:8000/docs
- **Data**: products.csv (1000 products)
- **Categories**: 8 categories

### gRPC
- **Port**: 50051
- **Proto file**: grpc-demo/protos/user_service.proto
- **RPC Patterns**: 4 types demonstrated
- **Sample Users**: 5 pre-loaded

### GraphQL
- **Port**: 8000
- **Endpoint**: http://localhost:8000/graphql
- **Playground**: Interactive browser-based IDE
- **Queries**: 7 queries, 5 mutations
- **Documentation**: 400+ line comprehensive guide

---

## Need Help?

- Check the README files for detailed documentation
- **Read GRAPHQL_EXPLAINED.md for comprehensive GraphQL guide**
- Review the code comments
- Look at the example requests
- Try the 40+ sample queries in SAMPLE_QUERIES.md

Happy coding! 🚀

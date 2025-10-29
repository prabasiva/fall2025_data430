#!/bin/bash

# Simple script to run the gRPC demo

echo "======================================"
echo "gRPC Python Demo"
echo "======================================"
echo ""

# Check if dependencies are installed
if ! python -c "import grpc" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo ""
fi

# Check if proto files are generated
if [ ! -f "user_service_pb2.py" ] || [ ! -f "user_service_pb2_grpc.py" ]; then
    echo "Generating gRPC code from proto file..."
    python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/user_service.proto
    echo ""
fi

echo "Starting gRPC server..."
python server.py &
SERVER_PID=$!

# Wait for server to start
sleep 2

echo ""
echo "Running client demos..."
echo ""
python client.py

echo ""
echo "Stopping server..."
kill $SERVER_PID 2>/dev/null

echo ""
echo "Demo completed!"

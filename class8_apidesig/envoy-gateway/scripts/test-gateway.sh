#!/bin/bash

# Test script for Envoy API Gateway
# Tests all three API types through the gateway

echo "========================================="
echo "Envoy API Gateway - Test Script"
echo "========================================="
echo ""

# Colors for output
GREEN='\033[0.32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

GATEWAY_URL="http://localhost:10000"
CONTROL_PLANE_URL="http://localhost:8080"

# Function to test endpoint
test_endpoint() {
    local name=$1
    local url=$2
    local method=${3:-GET}
    local data=$4

    echo -e "${YELLOW}Testing: $name${NC}"
    echo "URL: $url"

    if [ "$method" == "POST" ] && [ -n "$data" ]; then
        response=$(curl -s -X POST "$url" -H "Content-Type: application/json" -d "$data" -w "\nHTTP_CODE:%{http_code}")
    else
        response=$(curl -s "$url" -w "\nHTTP_CODE:%{http_code}")
    fi

    http_code=$(echo "$response" | grep "HTTP_CODE" | cut -d: -f2)
    body=$(echo "$response" | sed '/HTTP_CODE/d')

    if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
        echo -e "${GREEN}✓ Success (HTTP $http_code)${NC}"
        echo "Response: $body" | head -c 200
        echo ""
    else
        echo -e "${RED}✗ Failed (HTTP $http_code)${NC}"
        echo "Response: $body"
    fi
    echo ""
}

echo "1. Testing Control Plane"
echo "-------------------------"
test_endpoint "Control Plane Status" "$CONTROL_PLANE_URL/status"
test_endpoint "List Services" "$CONTROL_PLANE_URL/services"
test_endpoint "List Proxies" "$CONTROL_PLANE_URL/proxies"

echo ""
echo "2. Testing REST API via Gateway"
echo "--------------------------------"
test_endpoint "Gateway Root" "$GATEWAY_URL/"
test_endpoint "REST - Categories" "$GATEWAY_URL/api/categories"
test_endpoint "REST - Products" "$GATEWAY_URL/api/products/category/Electronics"

echo ""
echo "3. Testing GraphQL API via Gateway"
echo "-----------------------------------"
test_endpoint "GraphQL - Hello Query" "$GATEWAY_URL/graphql" "POST" '{"query": "{ hello }"}'
test_endpoint "GraphQL - Users Query" "$GATEWAY_URL/graphql" "POST" '{"query": "{ users { name email } }"}'
test_endpoint "GraphQL - Nested Query" "$GATEWAY_URL/graphql" "POST" '{"query": "{ user(id: 1) { name posts { title } } }"}'

echo ""
echo "4. Testing Multiple Envoy Instances"
echo "------------------------------------"
test_endpoint "Envoy Proxy 1" "http://localhost:10000/"
test_endpoint "Envoy Proxy 2" "http://localhost:10002/"
test_endpoint "Envoy Proxy 3" "http://localhost:10004/"

echo ""
echo "5. Testing Envoy Admin Interfaces"
echo "----------------------------------"
test_endpoint "Envoy 1 Admin" "http://localhost:9901/stats/prometheus"
test_endpoint "Envoy 2 Admin" "http://localhost:9902/stats/prometheus"
test_endpoint "Envoy 3 Admin" "http://localhost:9903/stats/prometheus"

echo ""
echo "========================================="
echo "Test Summary"
echo "========================================="
echo "All tests completed!"
echo ""
echo "Access Points:"
echo "  - Gateway (Proxy 1): http://localhost:10000"
echo "  - Gateway (Proxy 2): http://localhost:10002"
echo "  - Gateway (Proxy 3): http://localhost:10004"
echo "  - Control Plane: http://localhost:8080"
echo "  - Envoy Admin 1: http://localhost:9901"
echo "  - Envoy Admin 2: http://localhost:9902"
echo "  - Envoy Admin 3: http://localhost:9903"
echo ""

# Product Inventory REST API

A FastAPI-based REST API for managing and querying product inventory data from a CSV file.

## Features

- Read product information from CSV file
- Get products by category
- Get product count per category
- Get top 5 products by sales in a category
- Get top 5 aging inventory items

## Data Structure

Each product contains:
- `product_id`: Unique product identifier
- `name`: Product name
- `category`: Product category
- `price`: Product price
- `quantity_in_stock`: Current stock quantity
- `sales`: Total number of sales
- `last_stock_date`: Date when product was last stocked
- `supplier`: Supplier name

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Generate the sample CSV file (1000 products):
```bash
python generate_products.py
```

3. Run the API:
```bash
python main.py
```

Or use uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### 1. Get Root Information
```
GET /
```
Returns API information and available endpoints.

### 2. Get Products by Category
```
GET /products/category/{category}
```
Example: `GET /products/category/Electronics`

### 3. Get Product Count per Category
```
GET /products/category-counts
```
Returns the number of products in each category, sorted by count.

### 4. Get Top 5 Products by Sales in a Category
```
GET /products/top-sales/{category}?limit=5
```
Example: `GET /products/top-sales/Electronics?limit=5`

Parameters:
- `limit` (optional): Number of products to return (default: 5, max: 20)

### 5. Get Top 5 Aging Inventory
```
GET /products/aging-inventory?limit=5
```
Returns products with the oldest stock dates (and quantity > 0).

Parameters:
- `limit` (optional): Number of products to return (default: 5, max: 20)

### 6. Get All Products (with pagination)
```
GET /products/all?skip=0&limit=100
```
Parameters:
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Number of records to return (default: 100, max: 1000)

### 7. Get All Categories
```
GET /categories
```
Returns list of all available product categories.

## Interactive API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Example Usage

```bash
# Get all categories
curl http://localhost:8000/categories

# Get products in Electronics category
curl http://localhost:8000/products/category/Electronics

# Get product counts per category
curl http://localhost:8000/products/category-counts

# Get top 5 products by sales in Sports category
curl http://localhost:8000/products/top-sales/Sports?limit=5

# Get top 5 aging inventory items
curl http://localhost:8000/products/aging-inventory?limit=5
```

## Sample Categories

The generated data includes the following categories:
- Electronics
- Clothing
- Home & Kitchen
- Sports
- Books
- Toys
- Beauty
- Automotive

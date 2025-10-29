from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
import csv
from datetime import datetime
from pydantic import BaseModel

app = FastAPI(title="Product Inventory API", version="1.0.0")


class Product(BaseModel):
    product_id: str
    name: str
    category: str
    price: float
    quantity_in_stock: int
    sales: int
    last_stock_date: str
    supplier: str


class CategoryCount(BaseModel):
    category: str
    count: int


def load_products() -> List[Product]:
    """Load products from CSV file"""
    products = []
    try:
        with open('products.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                products.append(Product(
                    product_id=row['product_id'],
                    name=row['name'],
                    category=row['category'],
                    price=float(row['price']),
                    quantity_in_stock=int(row['quantity_in_stock']),
                    sales=int(row['sales']),
                    last_stock_date=row['last_stock_date'],
                    supplier=row['supplier']
                ))
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Products CSV file not found")
    return products


@app.get("/")
def root():
    """Root endpoint with API information"""
    return {
        "message": "Product Inventory API",
        "version": "1.0.0",
        "endpoints": {
            "/products/category/{category}": "Get all products in a category",
            "/products/category-counts": "Get product count for each category",
            "/products/top-sales/{category}": "Get top 5 products by sales in a category",
            "/products/aging-inventory": "Get top 5 aging inventory items"
        }
    }


@app.get("/products/category/{category}", response_model=List[Product])
def get_products_by_category(category: str):
    """Get all products in a specific category"""
    products = load_products()
    filtered_products = [p for p in products if p.category.lower() == category.lower()]

    if not filtered_products:
        raise HTTPException(status_code=404, detail=f"No products found in category: {category}")

    return filtered_products


@app.get("/products/category-counts", response_model=List[CategoryCount])
def get_category_counts():
    """Get the number of products in each category"""
    products = load_products()
    category_counts = {}

    for product in products:
        if product.category in category_counts:
            category_counts[product.category] += 1
        else:
            category_counts[product.category] = 1

    result = [CategoryCount(category=cat, count=count) for cat, count in category_counts.items()]
    return sorted(result, key=lambda x: x.count, reverse=True)


@app.get("/products/top-sales/{category}", response_model=List[Product])
def get_top_sales_by_category(category: str, limit: int = Query(default=5, ge=1, le=20)):
    """Get top products by sales in a specific category"""
    products = load_products()
    filtered_products = [p for p in products if p.category.lower() == category.lower()]

    if not filtered_products:
        raise HTTPException(status_code=404, detail=f"No products found in category: {category}")

    # Sort by sales in descending order
    sorted_products = sorted(filtered_products, key=lambda x: x.sales, reverse=True)

    return sorted_products[:limit]


@app.get("/products/aging-inventory", response_model=List[Product])
def get_aging_inventory(limit: int = Query(default=5, ge=1, le=20)):
    """Get top aging inventory items (oldest stock dates with quantity > 0)"""
    products = load_products()

    # Filter products with stock available
    in_stock_products = [p for p in products if p.quantity_in_stock > 0]

    if not in_stock_products:
        raise HTTPException(status_code=404, detail="No products in stock")

    # Sort by last_stock_date (oldest first)
    sorted_products = sorted(in_stock_products, key=lambda x: datetime.strptime(x.last_stock_date, "%Y-%m-%d"))

    return sorted_products[:limit]


@app.get("/products/all", response_model=List[Product])
def get_all_products(skip: int = Query(default=0, ge=0), limit: int = Query(default=100, ge=1, le=1000)):
    """Get all products with pagination"""
    products = load_products()
    return products[skip:skip + limit]


@app.get("/categories")
def get_categories():
    """Get list of all available categories"""
    products = load_products()
    categories = list(set(p.category for p in products))
    return {"categories": sorted(categories)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

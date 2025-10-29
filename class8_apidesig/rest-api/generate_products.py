import csv
import random
from datetime import datetime, timedelta

# Product categories
categories = ["Electronics", "Clothing", "Home & Kitchen", "Sports", "Books", "Toys", "Beauty", "Automotive"]

# Sample product names by category
product_names = {
    "Electronics": ["Laptop", "Smartphone", "Tablet", "Headphones", "Camera", "Monitor", "Keyboard", "Mouse", "Speaker", "Charger"],
    "Clothing": ["T-Shirt", "Jeans", "Jacket", "Dress", "Shoes", "Socks", "Hat", "Sweater", "Shorts", "Coat"],
    "Home & Kitchen": ["Blender", "Coffee Maker", "Toaster", "Microwave", "Pan", "Pot", "Knife Set", "Plate Set", "Cup", "Fork Set"],
    "Sports": ["Basketball", "Football", "Tennis Racket", "Yoga Mat", "Dumbbell", "Running Shoes", "Bicycle", "Helmet", "Water Bottle", "Gym Bag"],
    "Books": ["Fiction Novel", "Biography", "Cookbook", "Self-Help", "Mystery", "Science Fiction", "History", "Poetry", "Dictionary", "Atlas"],
    "Toys": ["Action Figure", "Doll", "Board Game", "Puzzle", "Building Blocks", "Remote Car", "Stuffed Animal", "Ball", "Kite", "Play-Doh"],
    "Beauty": ["Lipstick", "Moisturizer", "Shampoo", "Perfume", "Face Mask", "Nail Polish", "Sunscreen", "Eye Shadow", "Foundation", "Hair Dryer"],
    "Automotive": ["Oil Filter", "Air Filter", "Brake Pads", "Wiper Blades", "Battery", "Tire", "Spark Plug", "Car Cover", "Floor Mats", "Phone Mount"]
}

# Generate 1000 products
products = []
for i in range(1, 1001):
    category = random.choice(categories)
    product_name = random.choice(product_names[category])

    # Generate data
    product_id = f"PROD{i:04d}"
    name = f"{product_name} {random.choice(['Pro', 'Elite', 'Premium', 'Standard', 'Basic', 'Deluxe'])}"
    price = round(random.uniform(5.99, 999.99), 2)
    quantity_in_stock = random.randint(0, 500)
    sales = random.randint(0, 1000)

    # Generate last_stock_date (for aging inventory calculation)
    days_ago = random.randint(1, 730)  # Up to 2 years ago
    last_stock_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")

    supplier = random.choice(["Supplier A", "Supplier B", "Supplier C", "Supplier D", "Supplier E"])

    products.append({
        "product_id": product_id,
        "name": name,
        "category": category,
        "price": price,
        "quantity_in_stock": quantity_in_stock,
        "sales": sales,
        "last_stock_date": last_stock_date,
        "supplier": supplier
    })

# Write to CSV
with open('products.csv', 'w', newline='') as csvfile:
    fieldnames = ["product_id", "name", "category", "price", "quantity_in_stock", "sales", "last_stock_date", "supplier"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for product in products:
        writer.writerow(product)

print("Generated products.csv with 1000 products")

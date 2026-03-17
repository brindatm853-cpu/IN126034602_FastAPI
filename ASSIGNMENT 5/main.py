from fastapi import FastAPI, Query
from typing import Optional, List

app = FastAPI()

# Sample product data
products = [
    {"product_id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics"},
    {"product_id": 2, "name": "Notebook", "price": 99, "category": "Stationery"},
    {"product_id": 3, "name": "USB Hub", "price": 799, "category": "Electronics"},
    {"product_id": 4, "name": "Pen Set", "price": 49, "category": "Stationery"},
]

# Sample orders list
orders = []


# ---------------- Q1: Search Products ----------------
@app.get("/products/search")
def search_products(keyword: str):
    results = [p for p in products if keyword.lower() in p["name"].lower()]
    if not results:
        return {"message": f"No products found for: {keyword}"}
    return {"keyword": keyword, "total_found": len(results), "products": results}


# ---------------- Q2: Sort Products ----------------
@app.get("/products/sort")
def sort_products(sort_by: str = "price", order: str = "asc"):
    if sort_by not in ["price", "name"]:
        return {"error": "sort_by must be 'price' or 'name'"}
    reverse = order == "desc"
    sorted_products = sorted(products, key=lambda p: p[sort_by], reverse=reverse)
    return {"sort_by": sort_by, "order": order, "products": sorted_products}


# ---------------- Q3: Pagination ----------------
@app.get("/products/page")
def paginate_products(page: int = 1, limit: int = 2):
    total_products = len(products)
    total_pages = (total_products + limit - 1) // limit
    start = (page - 1) * limit
    end = start + limit
    paged = products[start:end]
    return {
        "page": page,
        "limit": limit,
        "total_products": total_products,
        "total_pages": total_pages,
        "products": paged
    }


# ---------------- Q4: Search Orders ----------------
@app.post("/orders")
def create_order(order: dict):
    order_id = len(orders) + 1
    order["order_id"] = order_id
    orders.append(order)
    return order

@app.get("/orders/search")
def search_orders(customer_name: str):
    results = [o for o in orders if customer_name.lower() in o["customer_name"].lower()]
    if not results:
        return {"message": f"No orders found for: {customer_name}"}
    return {"customer_name": customer_name, "total_found": len(results), "orders": results}


# ---------------- Q5: Sort by Category then Price ----------------
@app.get("/products/sort-by-category")
def sort_by_category():
    sorted_products = sorted(products, key=lambda p: (p["category"], p["price"]))
    return {"products": sorted_products}


# ---------------- Q6: Browse (Search + Sort + Pagination) ----------------
@app.get("/products/browse")
def browse_products(
    keyword: Optional[str] = None,
    sort_by: str = "price",
    order: str = "asc",
    page: int = 1,
    limit: int = 4
):
    filtered = products
    if keyword:
        filtered = [p for p in products if keyword.lower() in p["name"].lower()]

    reverse = order == "desc"
    if sort_by in ["price", "name"]:
        filtered = sorted(filtered, key=lambda p: p[sort_by], reverse=reverse)

    total_found = len(filtered)
    total_pages = (total_found + limit - 1) // limit
    start = (page - 1) * limit
    end = start + limit
    paged = filtered[start:end]

    return {
        "keyword": keyword,
        "sort_by": sort_by,
        "order": order,
        "page": page,
        "limit": limit,
        "total_found": total_found,
        "total_pages": total_pages,
        "products": paged
    }


# ---------------- ⭐ Bonus: Orders Pagination ----------------
@app.get("/orders/page")
def paginate_orders(page: int = 1, limit: int = 3):
    total_orders = len(orders)
    total_pages = (total_orders + limit - 1) // limit
    start = (page - 1) * limit
    end = start + limit
    paged = orders[start:end]
    return {
        "page": page,
        "limit": limit,
        "total_orders": total_orders,
        "total_pages": total_pages,
        "orders": paged
    }


# ---------------- Product by ID ----------------
@app.get("/products/{product_id}")
def get_product(product_id: int):
    for p in products:
        if p["product_id"] == product_id:
            return p
    return {"message": f"Product with id {product_id} not found"}
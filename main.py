import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Any

from fastmcp import FastMCP

mcp = FastMCP("Demo MCP Server")

DB_PATH = os.path.join(os.getenv("DATABASE_PATH", "."), "demo.db")

@mcp.tool()
def list_users() -> str:
    """List all users in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, age, created_at FROM users")
    users = cursor.fetchall()
    conn.close()
    
    if not users:
        return "No users found in the database."
    
    result = "Users in database:\n"
    for user in users:
        result += f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Age: {user[3]}, Created: {user[4]}\n"
    
    return result

@mcp.tool()
def list_products() -> str:
    """List all products in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price, category, in_stock FROM products")
    products = cursor.fetchall()
    conn.close()
    
    if not products:
        return "No products found in the database."
    
    result = "Products in database:\n"
    for product in products:
        stock_status = "In Stock" if product[4] else "Out of Stock"
        result += f"ID: {product[0]}, Name: {product[1]}, Price: ${product[2]}, Category: {product[3]}, Status: {stock_status}\n"
    
    return result

@mcp.tool()
def add_user(name: str, email: str, age: int) -> str:
    """Add a new user to the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        created_at = datetime.now().isoformat()
        cursor.execute(
            "INSERT INTO users (name, email, age, created_at) VALUES (?, ?, ?, ?)",
            (name, email, age, created_at)
        )
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return f"User '{name}' added successfully with ID: {user_id}"
    except sqlite3.IntegrityError:
        return f"Error: Email '{email}' already exists in the database."
    except Exception as e:
        return f"Error adding user: {str(e)}"

@mcp.tool()
def search_products_by_category(category: str) -> str:
    """Search for products by category."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, price, in_stock FROM products WHERE category = ? COLLATE NOCASE",
        (category,)
    )
    products = cursor.fetchall()
    conn.close()
    
    if not products:
        return f"No products found in category '{category}'."
    
    result = f"Products in category '{category}':\n"
    for product in products:
        stock_status = "In Stock" if product[3] else "Out of Stock"
        result += f"ID: {product[0]}, Name: {product[1]}, Price: ${product[2]}, Status: {stock_status}\n"
    
    return result

@mcp.tool()
def get_database_stats() -> str:
    """Get statistics about the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM products")
    product_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM products WHERE in_stock = 1")
    in_stock_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT AVG(age) FROM users WHERE age IS NOT NULL")
    avg_age = cursor.fetchone()[0]
    avg_age = round(avg_age, 1) if avg_age else 0
    
    conn.close()
    
    return f"""Database Statistics:
- Total Users: {user_count}
- Total Products: {product_count}
- Products In Stock: {in_stock_count}
- Average User Age: {avg_age} years
- Database File: {DB_PATH}"""

@mcp.tool()
def execute_custom_query(query: str) -> str:
    """Execute a custom SELECT query on the database. Only SELECT statements are allowed for safety."""
    query_stripped = query.strip().upper()
    if not query_stripped.startswith('SELECT'):
        return "Error: Only SELECT queries are allowed for safety reasons."
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        conn.close()
        
        if not results:
            return "Query executed successfully but returned no results."
        
        result = f"Query Results ({len(results)} rows):\n"
        result += " | ".join(columns) + "\n"
        result += "-" * (len(" | ".join(columns))) + "\n"
        
        for row in results:
            result += " | ".join(str(item) for item in row) + "\n"
        
        return result
        
    except Exception as e:
        return f"Error executing query: {str(e)}"

if __name__ == "__main__":
    mcp.run()

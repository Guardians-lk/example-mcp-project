import sqlite3
from datetime import datetime

DB_PATH = "demo.db"

def create_tables():
    """Create the database tables (migrations)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            age INTEGER,
            created_at TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            category TEXT NOT NULL,
            in_stock INTEGER DEFAULT 1
        )
    """)
    
    conn.commit()
    conn.close()
    print("Database tables created successfully!")

def seed_data():
    """Insert sample data into the database (seeders)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM products")
    product_count = cursor.fetchone()[0]
    
    if user_count == 0:
        sample_users = [
            ("Alice Johnson", "alice@example.com", 28, datetime.now().isoformat()),
            ("Bob Smith", "bob@example.com", 34, datetime.now().isoformat()),
            ("Carol Davis", "carol@example.com", 22, datetime.now().isoformat()),
            ("David Wilson", "david@example.com", 31, datetime.now().isoformat()),
            ("Emma Brown", "emma@example.com", 26, datetime.now().isoformat()),
        ]
        cursor.executemany(
            "INSERT INTO users (name, email, age, created_at) VALUES (?, ?, ?, ?)",
            sample_users
        )
        print(f"Inserted {len(sample_users)} sample users")
    else:
        print(f"Users table already has {user_count} records, skipping user seeding")
    
    if product_count == 0:
        sample_products = [
            ("Laptop", 999.99, "Electronics", 1),
            ("Coffee Mug", 12.50, "Kitchen", 1),
            ("Notebook", 5.99, "Office", 1),
            ("Wireless Mouse", 29.99, "Electronics", 0),
            ("Desk Lamp", 45.00, "Office", 1),
            ("Smartphone", 599.99, "Electronics", 1),
            ("Water Bottle", 18.75, "Kitchen", 1),
        ]
        cursor.executemany(
            "INSERT INTO products (name, price, category, in_stock) VALUES (?, ?, ?, ?)",
            sample_products
        )
        print(f"Inserted {len(sample_products)} sample products")
    else:
        print(f"Products table already has {product_count} records, skipping product seeding")
    
    conn.commit()
    conn.close()

def reset_database():
    """Drop all tables and recreate them (useful for development)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("DROP TABLE IF EXISTS products")
    
    conn.commit()
    conn.close()
    print("Database tables dropped")
    
    create_tables()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python database.py migrate    - Create tables")
        print("  python database.py seed       - Insert sample data")
        print("  python database.py reset      - Drop and recreate tables")
        print("  python database.py setup      - Run migrate + seed")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "migrate":
        create_tables()
    elif command == "seed":
        seed_data()
    elif command == "reset":
        reset_database()
    elif command == "setup":
        create_tables()
        seed_data()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

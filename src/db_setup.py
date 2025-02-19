import sqlite3
import os
import qrcode

DB_NAME = "supermarket.db"

# Ensure the static/qr_codes directory exists
QR_CODE_DIR = "static/qr_codes"
os.makedirs(QR_CODE_DIR, exist_ok=True)

def create_tables():
   
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        barcode TEXT UNIQUE NOT NULL,
        qr_code TEXT UNIQUE NOT NULL,  
        image TEXT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cart (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        quantity INTEGER DEFAULT 1,
        FOREIGN KEY (product_id) REFERENCES products (id)
    )""")

    conn.commit()
    conn.close()
    print("Database tables created successfully.")

def generate_qr_code(barcode):
 
    qr = qrcode.make(barcode)
    qr_path = f"{QR_CODE_DIR}/{barcode}.png"
    qr.save(qr_path)
    return qr_path

def insert_sample_products():
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    sample_products = [
        ("Apple", 1.5, "1234567890", "static/apple.png"),
        ("Bread", 2.0, "0987654321", "static/bread.png"),
        ("Milk", 3.0, "5678901234", "static/milk.png"),
        ("Rice", 5.0, "3456789012", "static/rice.png"),
        ("Juice", 2.5, "6789012345", "static/juice.png")
    ]

    # Generate QR codes and store the file paths
    products_with_qr = []
    for name, price, barcode, image in sample_products:
        qr_code_path = generate_qr_code(barcode)  # Generate QR
        products_with_qr.append((name, price, barcode, qr_code_path, image))

    cursor.executemany("""
    INSERT OR IGNORE INTO products (name, price, barcode, qr_code, image)
    VALUES (?, ?, ?, ?, ?)
    """, products_with_qr)

    conn.commit()
    conn.close()
    print("Sample products inserted successfully.")

if __name__ == "__main__":
    create_tables()
    insert_sample_products()

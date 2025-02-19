from flask import Flask, request, jsonify, render_template
import sqlite3
import os
from barcode_scanner import start_barcode_scanner
from QRcode_scanner import start_qr_code_scanner
from hal import hal_rfid_reader as rfid_reader
from hal import hal_lcd as LCD
from hal import hal_buzzer as buzzer

app = Flask(__name__)
DB_NAME = "supermarket.db"

# Function to connect to the database
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def homepage():
    """Render the main website homepage."""
    return render_template("homepage.html")

@app.route("/login")
def login():
    """Render the login page."""
    return render_template("login.html")

@app.route("/products")
def get_products():
    """Fetch product list from the database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        return jsonify([dict(row) for row in products])
    except sqlite3.Error as e:
        return jsonify({"error": str(e)})
    finally:
        conn.close()

@app.route("/scan_barcode", methods=["POST"])
def scan_barcode():
    """Triggers barcode scanning and retrieves product details."""
    barcode_data = start_barcode_scanner()
    if barcode_data:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE barcode=?", (barcode_data,))
        product = cursor.fetchone()
        conn.close()

        if product:
            return jsonify({"product_name": product["name"], "price": product["price"]})
        else:
            return jsonify({"error": "Product not found"}), 404
    return jsonify({"error": "Failed to scan"}), 500

@app.route("/scan_qr", methods=["POST"])
def scan_qr():
    """Triggers QR code scanning for order verification."""
    qr_data = start_qr_code_scanner()
    if qr_data:
        return jsonify({"order_verified": True, "order_id": qr_data})
    return jsonify({"error": "Invalid QR Code"}), 400

@app.route("/process_payment", methods=["POST"])
def process_payment():
    """Processes payment using RFID."""
    lcd = LCD.lcd()
    buzzer.beep(0.5, 0.2, 1)
    lcd.lcd_display_string("Scan RFID", 1)
    
    reader = rfid_reader.init()
    rfid_id = reader.read_id_no_block()
    
    if rfid_id:
        rfid_id_str = str(rfid_id).strip()
        buzzer.beep(0.5, 0.2, 1)
        print(f"RFID Scanned: {rfid_id_str}")
        lcd.lcd_clear()
        lcd.lcd_display_string("Payment Approved", 1)
        return jsonify({"payment_success": True, "rfid_id": rfid_id_str})
    
    lcd.lcd_clear()
    lcd.lcd_display_string("Payment Failed!", 1)
    buzzer.beep(0.5, 0.2, 2)
    return jsonify({"payment_success": False})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

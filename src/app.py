from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import os
import qrcode
from barcode_scanner import start_barcode_scanner
from QRcode_scanner import start_qr_code_scanner
from hal import hal_rfid_reader as rfid_reader
from hal import hal_lcd as LCD
from hal import hal_buzzer as buzzer
from hal import hal_keypad as keypad
import time
import RPi.GPIO as GPIO


app = Flask(__name__)
CORRECT_PIN = "1111"
DB_NAME = "supermarket.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def process_rfid_payment():
    """Handles payment using RFID only (No PIN fallback)."""
    lcd = LCD.lcd()
    lcd.lcd_clear()
    lcd.lcd_display_string("Scan RFID", 1)
    time.sleep(2)
    GPIO.setmode(GPIO.BCM)  # Ensure GPIO mode is set
    GPIO.setup(18, GPIO.OUT)  # Ensure buzzer pin is set 

    # Initialize RFID reader and scan for a card
    reader = rfid_reader.init()
    rfid_id = reader.read_id_no_block()

    if rfid_id:
        rfid_id_str = str(rfid_id).strip()  # Convert to string & remove spaces
        buzzer.beep(0.5, 0.2, 1)
        print(f"RFID Scanned: {rfid_id_str}")  # Debugging
        lcd.lcd_clear()
        lcd.lcd_display_string("Payment Approved", 1)
        time.sleep(2)
        return True  # Payment Successful

    # If no RFID is detected
    lcd.lcd_clear()
    lcd.lcd_display_string("Payment Failed!", 1)
    buzzer.beep(0.5, 0.2, 2)
    time.sleep(2)
    return False  # Payment Failed

# ------------------- HOMEPAGE -------------------
@app.route("/")
def homepage():
    """Show products on the homepage"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price, image FROM products LIMIT 5")
    products = cursor.fetchall()
    conn.close()
    return render_template("homepage.html", products=products)

# ------------------- CART -------------------
@app.route("/cart")
def view_cart():
    """Show the cart items."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT cart.id, products.name, products.price, cart.quantity FROM cart JOIN products ON cart.product_id = products.id")
    cart_items = cursor.fetchall()
    conn.close()
    return render_template("cart.html", cart_items=cart_items)

@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    """Add an item to the cart."""
    product_id = request.form.get("product_id")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cart (product_id, quantity) VALUES (?, 1)", (product_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("view_cart"))

def process_pin_payment():
    GPIO.setmode(GPIO.BCM)  # Ensure GPIO mode is set
    GPIO.setup(18, GPIO.OUT)  # Ensure buzzer pin is set
    lcd = LCD.lcd()
    lcd.lcd_clear()
    lcd.lcd_display_string("Enter PIN", 1)
    time.sleep(5)

    entered_pin = request.json.get("pin", "")  # Get PIN from request

    if entered_pin == CORRECT_PIN:
        buzzer.beep(0.5, 0.2, 1)
        lcd.lcd_clear()
        lcd.lcd_display_string("Payment Approved", 1)
        time.sleep(8)
        return True  # Payment Successful
    else:
        lcd.lcd_clear()
        lcd.lcd_display_string("Wrong PIN!", 1)
        buzzer.beep(0.5, 0.2, 2)
        time.sleep(2)
        return False  # Payment Failed

# ------------------- CHECKOUT & QR CODE -------------------
@app.route("/checkout")
def checkout():
    """Checkout page displaying a fixed QR Code for payment without generating it."""
    # Use the pre-existing payment QR code stored in static/
    qr_code_path = "payment.png"

    return render_template("checkout.html", qr_code_path=qr_code_path)



# ------------------- PROCESS PAYMENT -------------------
@app.route("/process_payment", methods=["POST"])
def process_payment():
    payment_method = request.json.get("payment_method")

    if payment_method == "rfid":
        success = process_rfid_payment()
    elif payment_method == "pin":
        success = process_pin_payment()
    else:
        success = False

    if success:
        return jsonify({"status": "success", "message": "Payment Successful"})
    else:
        return jsonify({"status": "failed", "message": "Payment Failed"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

    

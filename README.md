Supermarket Self-Checkout System - Printable Notes
Project Overview:
The Supermarket Self-Checkout System allows customers to scan barcodes for in-store purchases and QR codes for online orders. The system supports payments via RFID or a PIN entry system, displaying transactions on an LCD screen.

Features:

Barcode scanning for in-store purchases
QR code verification for online orders
RFID-based contactless payments
PIN-based payment option (Default: 8888)
LCD display for transaction details
Receipt printing on LCD
Buzzer for confirmation feedback

Hardware Components:
PiCamera for barcode/QR scanning
LCD Display
Keypad
RFID Reader & Cards
Buzzer

How to Use the System:
Startup
System initializes and displays "Supermarket Self-Checkout"
Waits for user input

Select Mode:
Press 1 to scan a barcode (in-store purchase)
Press 2 to scan a QR code (online order verification)

Scanning Process:
Barcode Scanner: Detects product barcode and displays name & price
QR Code Scanner: Verifies online purchase

Payment Selection:
Press 1 to pay with RFID (Tap your card)
Press 2 to pay with PIN (Enter 4-digit code, default: 8888)

Transaction Completion:
If successful, "Payment Approved" is displayed
If failed, "Payment Failed" message is shown with buzzer alert
LCD displays receipt with product name and price

Troubleshooting Guide:
Barcode/QR not scanning?
Ensure proper lighting
Check camera connection
Restart system if needed

System Commands 
Start Program: python main.py
Start Flask app: python app.py


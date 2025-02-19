import time
from threading import Thread
import queue
from hal import hal_lcd as LCD
from hal import hal_keypad as keypad
from hal import hal_buzzer as buzzer
from hal import hal_rfid_reader as rfid_reader
from barcode_scanner import start_barcode_scanner
from QRcode_scanner import start_qr_code_scanner
import RPi.GPIO as GPIO

# Shared queue for keypad inputs
shared_keypad_queue = queue.Queue()

# Initialize LCD
lcd = LCD.lcd()
lcd.lcd_clear()

# Callback function to capture keypad presses
def key_pressed(key):
    shared_keypad_queue.put(key)

def process_payment():
    """Handles payment via RFID or PIN input."""
    lcd.lcd_clear()
    lcd.lcd_display_string("1.RFID  2.PIN", 1)
    
    key = shared_keypad_queue.get()
    if key == 1:
        return process_rfid_payment()
    elif key == 2:
        return process_pin_payment()
    else:
        lcd.lcd_display_string("Invalid Option!", 1)
        buzzer.beep(0.5, 0.2, 2)
        time.sleep(2)
        return False

def process_rfid_payment():
    """Handles payment via RFID."""
    GPIO.setmode(GPIO.BCM)  # Ensure GPIO mode is set
    GPIO.setup(18, GPIO.OUT)  # Ensure buzzer pin is set 
    lcd.lcd_clear()
    lcd.lcd_display_string("Scan RFID", 1)
    reader = rfid_reader.init()
    rfid_id = reader.read_id_no_block()
    
    if rfid_id:
        buzzer.beep(0.5, 0.2, 1)
        lcd.lcd_clear()
        lcd.lcd_display_string("Payment Approved", 1)
        time.sleep(2)
        return True
    else:
        lcd.lcd_display_string("Payment Failed!", 1)
        buzzer.beep(0.5, 0.2, 2)
        time.sleep(2)
        return False

def process_pin_payment():
    """Handles payment via PIN input."""
    GPIO.setmode(GPIO.BCM)  # Ensure GPIO mode is set
    GPIO.setup(18, GPIO.OUT)  # Ensure buzzer pin is set
    lcd.lcd_clear()
    lcd.lcd_display_string("Enter PIN:", 1)
    entered_pin = ""

    while len(entered_pin) < 4:
        key = shared_keypad_queue.get()
        entered_pin += str(key)
        lcd.lcd_display_string("*" * len(entered_pin), 2)
    
    lcd.lcd_display_string("Processing...", 1)
    time.sleep(2)
    
    if entered_pin == "8888":  # Correct PIN
        lcd.lcd_clear()
        lcd.lcd_display_string("Payment Approved", 1)
        time.sleep(2)
        return True
    else:
        lcd.lcd_display_string("Invalid PIN!", 1)
        buzzer.beep(0.5, 0.2, 2)
        time.sleep(2)
        return False

def print_receipt(item_name, price):
    """Prints receipt on LCD."""
    lcd.lcd_clear()
    lcd.lcd_display_string("Receipt:", 1)
    lcd.lcd_display_string(f"{item_name}", 2)
    time.sleep(2)
    lcd.lcd_display_string(f"Price: ${price}", 2)
    time.sleep(2)
    lcd.lcd_display_string("Thank You!", 1)
    time.sleep(2)

def handle_barcode_purchase():
    """Handles barcode scanning and payment process."""
    lcd.lcd_display_string("Scanning Barcode...", 1)
    barcode_data = start_barcode_scanner()
    
    if barcode_data:
        lcd.lcd_display_string(f"Item: {barcode_data}", 1)
        lcd.lcd_display_string("Price: $5.00", 2)  # Fixed price for demo
        time.sleep(2)
        
        lcd.lcd_display_string("Proceed to Pay?", 1)
        lcd.lcd_display_string("1.Yes 2.No", 2)
        key = shared_keypad_queue.get()
        
        if key == 1:
            if process_payment():
                print_receipt(barcode_data, "5.00")
    else:
        lcd.lcd_display_string("Scan Failed!", 1)
    time.sleep(2)

def handle_qr_code_verification():
    """Handles QR Code scanning and payment process."""
    lcd.lcd_display_string("Scanning QR Code...", 1)
    order_id = start_qr_code_scanner()
    
    if order_id:
        lcd.lcd_display_string("Order Verified", 1)
        time.sleep(2)
        
        lcd.lcd_display_string("Proceed to Pay?", 1)
        lcd.lcd_display_string("1.Yes 2.No", 2)
        key = shared_keypad_queue.get()

        if key == 1:
            if process_payment():
                print_receipt("Online Order", "10.00")
    else:
        lcd.lcd_display_string("Invalid QR Code!", 1)
    time.sleep(2)

def main():
    """Main function for self-checkout system."""
    keypad.init(key_pressed)
    keypad_thread = Thread(target=keypad.get_key)
    keypad_thread.daemon = True
    keypad_thread.start()

    lcd.lcd_clear()
    lcd.lcd_display_string("Supermarket", 1)
    lcd.lcd_display_string("Self-Checkout", 2)
    time.sleep(3)

    while True:
        lcd.lcd_clear()
        lcd.lcd_display_string("1.Barcode 2.QR", 1)

        keyvalue = shared_keypad_queue.get()
        if keyvalue == 1:
            handle_barcode_purchase()
        elif keyvalue == 2:
            handle_qr_code_verification()

if __name__ == '__main__':
    main()

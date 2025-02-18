import time
from threading import Thread
import queue

# Import HAL modules
from hal import hal_led as led
from hal import hal_lcd as LCD
from hal import hal_adc as adc
from hal import hal_buzzer as buzzer
from hal import hal_keypad as keypad
from hal import hal_rfid_reader as rfid_reader
from hal import hal_servo as servo
from hal import hal_dc_motor as dc_motor

# Import functional modules
from barcode_scanner import start_barcode_scanner
from QRcode_scanner import start_qr_code_scanner
from payment_processor import process_payment

# Shared queue for keypad presses
shared_keypad_queue = queue.Queue()

# Callback function invoked when a key is pressed
def key_pressed(key):
    shared_keypad_queue.put(key)

def main():
    # Initialize hardware components
    led.init()
    adc.init()
    buzzer.init()
    rfid_reader.init()
    servo.init()
    dc_motor.init()
    
    keypad.init(key_pressed)
    keypad_thread = Thread(target=keypad.get_key)
    keypad_thread.start()

    lcd = LCD.lcd()
    lcd.lcd_clear()

    lcd.lcd_display_string("Supermarket", 1)
    lcd.lcd_display_string("Self-Checkout", 2)
    time.sleep(3)

    print("Press 1 to Scan Barcode")
    print("Press 2 to Scan QR Code")
    print("Press 3 to Process Payment")
    print("Press 4 to Open Servo (Dispense)")
    print("Press 5 to Control DC Motor")
    print("Press * to Exit")

    while True:
        lcd.lcd_clear()
        lcd.lcd_display_string("Select an Option", 1)
        print("Waiting for key press...")
        
        keyvalue = shared_keypad_queue.get()
        print(f"Key Pressed: {keyvalue}")

        if keyvalue == 1:
            lcd.lcd_display_string("Scanning Barcode...", 1)
            barcode_data = start_barcode_scanner()
            lcd.lcd_display_string(f"Scanned: {barcode_data}" if barcode_data else "Scan Failed!", 2)
            time.sleep(2)

        elif keyvalue == 2:
            lcd.lcd_display_string("Scanning QR Code...", 1)
            qr_data = start_qr_code_scanner()
            lcd.lcd_display_string(f"QR Verified: {qr_data}" if qr_data else "Invalid QR Code!", 2)
            time.sleep(10)

        elif keyvalue == 3:
            lcd.lcd_display_string("Processing Payment...", 1)
            payment_status = process_payment()
            lcd.lcd_display_string("Payment Successful" if payment_status else "Payment Failed!", 2)
            time.sleep(2)

        elif keyvalue == 4:
            lcd.lcd_display_string("Dispensing...", 1)
            servo.set_servo_position(90)  # Example dispensing angle
            time.sleep(2)
            servo.set_servo_position(0)
            lcd.lcd_display_string("Done!", 2)
            time.sleep(2)

        elif keyvalue == 5:
            lcd.lcd_display_string("Controlling Motor...", 1)
            dc_motor.set_motor_speed(50)  # Adjust motor speed as needed
            time.sleep(3)
            dc_motor.set_motor_speed(0)
            lcd.lcd_display_string("Stopped!", 2)
            time.sleep(2)

        elif keyvalue == "*":
            lcd.lcd_clear()
            lcd.lcd_display_string("Goodbye!", 1)
            time.sleep(2)
            break

        else:
            lcd.lcd_display_string("Invalid Option!", 1)
            buzzer.beep()
            time.sleep(1)

if __name__ == '__main__':
    main()

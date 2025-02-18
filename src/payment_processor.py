def process_payment(lcd, buzzer, rfid_reader):
    lcd.clear()
    lcd.write_line(1, "Tap Card or Enter PIN")
    
    card_id = rfid_reader.scan()
    if card_id:
        lcd.write_line(2, "Payment Successful")
    else:
        lcd.write_line(2, "Enter PIN")
        pin = input("Enter PIN: ")  # Replace with keypad input logic
        lcd.write_line(2, "Payment Approved" if pin == "1234" else "Payment Failed")
        buzzer.beep() if pin != "1234" else None

def admin_menu(lcd):
    lcd.clear()
    lcd.write_line(1, "Admin Menu")
    lcd.write_line(2, "1. View Logs")
    lcd.write_line(3, "2. Update Inventory")
    lcd.write_line(4, "3. Exit")

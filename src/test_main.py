import pytest
from unittest.mock import MagicMock
import time
from main import process_payment, key_pressed, main
import queue

@pytest.fixture
def mock_lcd():
    """Mock the LCD display."""
    lcd = MagicMock()
    return lcd

@pytest.fixture
def mock_buzzer():
    """Mock the Buzzer."""
    buzzer = MagicMock()
    return buzzer

@pytest.fixture
def mock_rfid_reader():
    """Mock the RFID Reader."""
    rfid_reader = MagicMock()
    rfid_reader.init.return_value.read_id_no_block.return_value = "12345"  # Simulate RFID scan success
    return rfid_reader

@pytest.fixture
def mock_keypad():
    """Mock the Keypad."""
    keypad = MagicMock()
    keypad.get_key.return_value = "1"
    return keypad

@pytest.fixture
def mock_barcode_scanner():
    """Mock Barcode Scanner function."""
    return MagicMock(return_value="123456789")

@pytest.fixture
def mock_qr_scanner():
    """Mock QR Code Scanner function."""
    return MagicMock(return_value="QR_ORDER_001")

def test_process_payment_success(mock_lcd, mock_buzzer, mock_rfid_reader):
    """Test the process_payment function for successful RFID payment."""
    result = process_payment(mock_lcd, mock_buzzer, mock_rfid_reader)
    
    # Assert LCD calls
    mock_lcd.lcd_display_string.assert_any_call("Scan RFID", 1)
    mock_lcd.lcd_display_string.assert_any_call("Payment Approved", 1)

    # Assert RFID reader call
    mock_rfid_reader.init.assert_called_once()

    # Assert buzzer is used
    mock_buzzer.beep.assert_called_once()

    assert result is True  # Ensure function returns True for success

def test_process_payment_fail(mock_lcd, mock_buzzer, mock_rfid_reader):
    """Test the process_payment function when RFID fails to scan."""
    mock_rfid_reader.init.return_value.read_id_no_block.return_value = None  # Simulate RFID scan failure

    result = process_payment(mock_lcd, mock_buzzer, mock_rfid_reader)

    # Assert LCD shows "Payment Failed"
    mock_lcd.lcd_display_string.assert_any_call("Payment Failed!", 1)

    # Assert buzzer beeped twice for failure
    mock_buzzer.beep.assert_called_with(0.5, 0.2, 2)

    assert result is False  # Ensure function returns False for failure
from main import shared_keypad_queue, key_pressed

def test_keypad_press():
    """Test that a keypress is correctly placed into the queue."""
    shared_keypad_queue.queue.clear()  # Clear queue before test
    key_pressed("5")

    assert not shared_keypad_queue.empty()
    assert shared_keypad_queue.get() == "5"



def test_barcode_scanner(mock_lcd, mock_barcode_scanner):
    """Test barcode scanning process."""
    barcode_data = mock_barcode_scanner()
    assert barcode_data == "123456789"

def test_qr_code_scanner(mock_lcd, mock_qr_scanner):
    """Test QR code scanning process."""
    qr_data = mock_qr_scanner()
    assert qr_data == "QR_ORDER_001"


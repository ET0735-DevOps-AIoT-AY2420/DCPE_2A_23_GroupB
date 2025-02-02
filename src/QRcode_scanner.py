from picamera2 import Picamera2, Preview
from pyzbar.pyzbar import decode
from PIL import Image
import numpy as np
import time

def process_frame(frame):
    """
    Decode QR codes from a single frame.
    """
    img = Image.fromarray(frame)  # Convert NumPy array to PIL Image
    decoded_objects = decode(img)
    for obj in decoded_objects:
        print(f"QR Code Type: {obj.type}, Data: {obj.data.decode('utf-8')}")
        return obj.data.decode("utf-8")  # Return the first decoded QR code
    return None

def start_qr_code_scanner():
    """
    Starts the QR code scanner with a live camera preview.
    """
    print("Initializing camera...")
    picam2 = Picamera2()

    # Configure the camera for preview and processing
    camera_config = picam2.create_preview_configuration(main={"size": (320, 240)})
    picam2.configure(camera_config)

    # Start the camera with a preview
    picam2.start_preview(Preview.QTGL)  # QTGL provides a hardware-accelerated preview window
    picam2.start()
    time.sleep(2)  # Allow the camera to stabilize

    print("Camera started. Scanning for QR codes...")
    try:
        while True:
            # Capture a frame as a NumPy array
            frame = picam2.capture_array()

            # Process the frame for QR codes
            qr_data = process_frame(frame)
            if qr_data:
                print(f"Decoded QR Code: {qr_data}")
                break  # Stop scanning once a QR code is decoded

            time.sleep(0.1)  # Reduce CPU usage

    except KeyboardInterrupt:
        print("\nQR code scanner stopped.")
    finally:
        picam2.stop_preview()
        picam2.stop()
        print("Camera stopped.")

if __name__ == "__main__":
    start_qr_code_scanner()

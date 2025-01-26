from picamera2 import Picamera2, Preview
from pyzbar.pyzbar import decode
from PIL import Image
import numpy as np
import time

def process_frame(frame):
    """
    Decode barcodes from a single frame.
    """
    img = Image.fromarray(frame)  # Convert NumPy array to PIL Image
    decoded_objects = decode(img)
    for obj in decoded_objects:
        print(f"Barcode Type: {obj.type}, Data: {obj.data.decode('utf-8')}")
        return obj.data.decode("utf-8")  # Return the first decoded barcode
    return None

def start_barcode_scanner():
    """
    Starts the barcode scanner with a live camera preview.
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

    print("Camera started. Scanning for barcodes...")
    try:
        while True:
            # Capture a frame as a NumPy array
            frame = picam2.capture_array()

            # Process the frame for barcodes
            barcode_data = process_frame(frame)
            if barcode_data:
                print(f"Decoded Barcode: {barcode_data}")
                break  # Stop scanning once a barcode is decoded

            time.sleep(0.1)  # Reduce CPU usage

    except KeyboardInterrupt:
        print("\nBarcode scanner stopped.")
    finally:
        picam2.stop_preview()
        picam2.stop()
        print("Camera stopped.")

if __name__ == "__main__":
    start_barcode_scanner()

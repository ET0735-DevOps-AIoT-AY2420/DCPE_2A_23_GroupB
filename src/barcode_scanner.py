from picamera2 import Picamera2
from pyzbar.pyzbar import decode
from PIL import Image
import time
import numpy as np

def process_frame(frame):
    """
    Process a single camera frame and decode barcodes.
    """
    # Convert frame (NumPy array) to PIL Image for decoding
    img = Image.fromarray(frame)

    # Decode barcodes in the image
    decoded_objects = decode(img)
    if not decoded_objects:
        return None

    # Process decoded barcodes
    for obj in decoded_objects:
        print(f"Barcode Type: {obj.type}, Data: {obj.data.decode('utf-8')}")
        return obj.data.decode("utf-8")

    return None

def start_barcode_scanner():
    """
    Starts the live barcode scanner using the Raspberry Pi camera.
    """
    print("Initializing camera...")
    picam2 = Picamera2()
    camera_config = picam2.create_preview_configuration(main={"size": (640, 480)})
    picam2.configure(camera_config)

    try:
        picam2.start()
        print("Camera started. Scanning for barcodes...")
        time.sleep(2)  # Allow the camera to stabilize

        while True:
            # Capture a frame
            frame = picam2.capture_array()

            # Process the frame for barcodes
            barcode_data = process_frame(frame)
            if barcode_data:
                print(f"Decoded Barcode: {barcode_data}")
                break  # Stop scanning after successfully decoding a barcode

            time.sleep(0.1)  # Reduce CPU usage

    except KeyboardInterrupt:
        print("\nBarcode scanner stopped.")
    finally:
        picam2.stop()
        print("Camera stopped.")

if __name__ == "__main__":
    start_barcode_scanner()

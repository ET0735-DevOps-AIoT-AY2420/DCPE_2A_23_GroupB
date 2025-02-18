import time
from picamera2 import Picamera2
from pyzbar.pyzbar import decode
import cv2

def start_barcode_scanner(scan_time=20):
    """
    Scans barcodes from the camera and returns the first detected barcode.
    :param scan_time: Time limit in seconds before stopping the scan.
    :return: Decoded barcode data or None if no barcode is detected.
    """
    print("📸 Initializing camera for barcode scanning...")

    picam2 = Picamera2()
    video_config = picam2.create_video_configuration(main={"size": (640, 480)})
    picam2.configure(video_config)

    scanning = True
    start_time = time.time()
    barcode_data = None

    # Start the camera
    picam2.start()

    try:
        while scanning:
            # Capture a frame
            frame = picam2.capture_array()

            # Convert frame to grayscale for better processing
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect barcodes in the frame
            codes = decode(gray)

            for code in codes:
                barcode_data = code.data.decode("utf-8")
                print(f"✅ Barcode Detected: {barcode_data}")
                scanning = False  # Stop scanning once a barcode is found
                break

            # Stop scanning if the time limit is exceeded
            if time.time() - start_time > scan_time:
                print("⏳ Scanning time exceeded!")
                scanning = False

            time.sleep(0.1)  # Reduce CPU usage

    except KeyboardInterrupt:
        print("\n🚫 Barcode scanner stopped manually.")

    finally:
        picam2.stop()
        picam2.close()
        print("📸 Camera stopped.")

    return barcode_data

if __name__ == "__main__":
    scanned_data = start_barcode_scanner(scan_time=20)
    if scanned_data:
        print(f"✅ Decoded Barcode: {scanned_data}")
    else:
        print("⚠️ No Barcode detected.")

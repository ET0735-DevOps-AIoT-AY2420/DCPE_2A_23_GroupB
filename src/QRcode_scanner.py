import time
from picamera2 import Picamera2
from pyzbar.pyzbar import decode
import cv2

def start_qr_code_scanner(scan_time=20):
    """
    Scans QR codes from the camera and returns the first detected code.
    :param scan_time: Time limit in seconds before stopping the scan.
    :return: Decoded QR code data or None if no QR code is detected.
    """
    print("Initializing camera for QR scanning...")
    
    picam2 = Picamera2()
    video_config = picam2.create_video_configuration(main={"size": (640, 480)})
    picam2.configure(video_config)
    
    scanning = True
    start_time = time.time()
    qr_data = None

    # Start the camera
    picam2.start()
    
    try:
        while scanning:
            # Capture a frame
            frame = picam2.capture_array()

            # Convert frame to grayscale for better processing
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect QR codes in the frame
            codes = decode(gray)

            for code in codes:
                qr_data = code.data.decode("utf-8")
                print(f"QR Code Detected: {qr_data}")
                scanning = False  # Stop scanning once a QR code is found
                break

            # Stop scanning if the time limit is exceeded
            if time.time() - start_time > scan_time:
                print("Scanning time exceeded!")
                scanning = False

            time.sleep(0.1)  # Reduce CPU usage

    except KeyboardInterrupt:
        print("\nQR code scanner stopped manually.")

    finally:
        picam2.stop()
        picam2.close()
        print("Camera stopped.")

    return qr_data

if __name__ == "__main__":
    scanned_data = start_qr_code_scanner(scan_time=20)
    if scanned_data:
        print(f"Decoded QR Code: {scanned_data}")
    else:
        print("No QR Code detected.")

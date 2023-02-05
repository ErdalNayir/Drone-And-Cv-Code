from ImageProcessing.ThreadCamera import ThreadCamera
import time

cap = ThreadCamera(src=0).start()

while True:
    cap.detect_mid_and_close()
    time.sleep(1)



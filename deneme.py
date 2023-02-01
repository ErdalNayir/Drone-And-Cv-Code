from ImageProcessing.ThreadCamera import ThreadCamera


cap = ThreadCamera(src=0).start()

cap.detect_mid_and_close()

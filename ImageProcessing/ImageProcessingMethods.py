import cv2
import numpy as np
import time

def denoiseImg(img):
    kernel = np.ones((5, 5), np.uint8)

    blurred_img = cv2.GaussianBlur(img,(7,7),0)
    img_erosion = cv2.erode(img, kernel, iterations=2)
    img_dilation = cv2.dilate(img_erosion, kernel, iterations=2)

    return img_dilation

def detectColor(frame):

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #lower = np.array([hMin, sMin, vMin])
    # upper = np.array([hMax, sMax, vMax])

    # Defining lower and upper bound HSV values
    lower = np.array([81, 90, 109])
    upper = np.array([103, 255, 255])

    # Defining mask for detecting color
    mask = cv2.inRange(hsv, lower, upper)

    return mask

def detectPosition(X,Y):
    if X <= 180 and Y <= 180:
        return "Kuzey Bati"
    elif X <= 180 and 180 < Y <= 360:
        return "Bati"
    if X <= 180 and 360 < Y <= 540:
        return "Guney Bati"

    if 180< X <= 360 and Y <= 180:
        return "Kuzey"
    elif 180< X <= 360 and 180 < Y <= 360:
        return "Merkez"
    if 180< X <= 360 and 360 < Y <= 540:
        return "Guney"

    if 360< X <= 540 and Y <= 180:
        return "Kuzey Dogu"
    elif 360< X <= 540 and 180 < Y <= 360:
        return "Dogu"
    if 360< X <= 540 and 360 < Y <= 540:
        return "Guney Dogu"

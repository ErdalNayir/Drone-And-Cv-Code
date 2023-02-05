import threading
import cv2
from ImageProcessingMethods import denoiseImg, detectColor, detectPosition,detect_line_position
from Counter import CenterCounter
import time


class ThreadCamera:
    def __init__(self, src=0, name="ColorDetection"):
        threading.Thread.__init__(self)

        # initialize the video camera stream and read the first frame
        # from the stream
        self.cap = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.cap.read()

        # initialize the thread name
        self.name = name

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        t = threading.Thread(target=self.update, name=self.name, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.cap.read()

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True

    def detect_mid_and_close(self):
        i = 0
        started = 0
        position_str=""
        _, self.frame = self.cap.read()
        # denoising imageq
        dni = denoiseImg(self.frame)
        # detect color
        new_frame = detectColor(dni)
        # get boundries
        contours, hierarchy = cv2.findContours(new_frame, 1, 2)
        # ObjectCounter:
        object_counter = 1
        # Creating bounding box and center circle
        for _, cnt in enumerate(contours):
            rect = cv2.boundingRect(cnt)
            if 2800 <= cv2.contourArea(cnt):
                if object_counter == 1:  # that code ensures that there is only one detected object on the screen
                    x, y, w, h = rect  # coordinates of bounding box
                    # coordinates of circle center
                    circle_x = int(x + w / 2)
                    circle_y = int(y + h / 2)
                    # position string that is come from custom function "detectPosition" and print out the text
                    # on screen
                    position_str = detect_line_position(circle_x)

                    # for every detected object that variable will be increased by one
                    object_counter += 1
        # show the image
        cv2.imshow("frame", self.frame)
        time.sleep(1)
        cv2.imshow("frame", self.frame)
        k= cv2.waitKey(1) & 0xFF == ord("q")

        return position_str

        cv2.destroyAllWindows()



    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cap.release()

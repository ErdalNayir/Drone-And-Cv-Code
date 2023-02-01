import threading
import cv2
from ImageProcessingMethods import denoiseImg, detectColor, detectPosition
from Counter import CenterCounter


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
        value = True
        while value:
            i += 1
            if self.stopped:
                return

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
                if 2800 <= cv2.contourArea(cnt) <= 8000:
                    if object_counter == 1:  # that code ensures that there is only one detected object on the screen
                        x, y, w, h = rect  # coordinates of bounding box
                        # coordinates of circle center
                        circle_x = int(x + w / 2)
                        circle_y = int(y + h / 2)
                        # position string that is came from custom function "detectPosition" and print out the text
                        # on screen
                        position_str = detectPosition(circle_x, circle_y)
                        if position_str != "Merkez":
                            cv2.putText(self.frame, position_str, (x + 10, y - 10), 5, 0.75, (0, 255, 0))
                            # drawing bounding box
                            cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                            # center of detected image's bounding box
                            cv2.circle(self.frame, (circle_x, circle_y), 5, (0, 255, 0), 2)
                            cv2.imshow("frame", self.frame)
                            # reseting started flag
                            started = 0
                        else:
                            if started == 0:
                                # threading task
                                thread_1 = CenterCounter(3)
                                thread_1.start()
                                started = 1
                            cv2.putText(self.frame, "Cikiliyor {}...".format(thread_1.counter), (x + 10, y - 10), 5,
                                        0.75,
                                        (0, 0, 255))
                            # drawing bounding box
                            cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                            # center of detected image's bounding box
                            cv2.circle(self.frame, (circle_x, circle_y), 5, (0, 0, 255), 2)
                            cv2.imshow("frame", self.frame)
                            if thread_1.counter == 0:
                                value = False
                        # for every detected object that variable will be increased by one
                        object_counter += 1
            # show the image
            cv2.imshow("frame", self.frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cap.release()

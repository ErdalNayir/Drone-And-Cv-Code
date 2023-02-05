#CREATED BY ERDAL NAYIR
import cv2
from ImageProcessingMethods import denoiseImg,detectColor,detectPosition
from Counter import CenterCounter


def startVideo():
    # define flag and variable
    started = 0
    cap =cv2.VideoCapture(0)
    value=True
    while(value):
        # read frame
        ret, frame = cap.read()
        frame = cv2.resize(frame,[540,540])
        # denoising imageq
        dni=denoiseImg(frame)
        # detect color
        newFrame = detectColor(dni)
        #get boundries
        contours, hiearcy = cv2.findContours(newFrame, 1, 2)
        # ObjectCounter:
        objectCounter = 1
        # Creating bounding box and center circle
        for _,cnt in enumerate(contours):
            rect = cv2.boundingRect(cnt)
            print((cv2.contourArea(cnt)))
            if cv2.contourArea(cnt)>=2800:

                if objectCounter==1: #that code ensures that there is only one detected object on the screen
                    x, y, w, h = rect # coordinates of bounding box
                    #coordinates of circle center
                    circleX = int(x + w / 2)
                    circleY = int(y + h / 2)
                    #position string that is came from custom function "detectPosition" and print out the text on screen
                    positionStr = detectPosition(circleX,circleY)
                    if positionStr!="Merkez":
                        cv2.putText(frame, positionStr, (x + 10, y - 10), 5, 0.75, (0, 255, 0))
                        #drawing bounding box
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        # center of detected image's bounding box
                        cv2.circle(frame, (circleX, circleY), 5, (0, 255, 0), 2)
                        cv2.imshow("frame", frame)
                        #reseting started flag
                        started=0
                    else:
                        if started==0:
                            #threading task
                            thread_1 = CenterCounter(3)
                            thread_1.start()
                            started=1
                        cv2.putText(frame, "Cikiliyor {}...".format(thread_1.counter), (x + 10, y - 10), 5, 0.75,(0, 0, 255))
                        # drawing bounding box
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                        # center of detected image's bounding box
                        cv2.circle(frame, (circleX, circleY), 5, (0, 0, 255), 2)
                        cv2.imshow("frame", frame)
                        if thread_1.counter ==0:
                            value=False
                    #for every detected object that variable will be increased by one
                    objectCounter += 1
        #show the image
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    # After the loop release the cap object
    cap.release()
    # Destroy all the windows
    cv2.destroyAllWindows()
# by this condition I ensure that this python file cannot be imported by other python files.
if __name__ == '__main__':
    #calling the function
    startVideo()
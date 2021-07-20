import cv2
import numpy as np
import imutils
from apriltag import apriltag
from skimage.filters import threshold_local

tagFamily = "tag36h11"

cap = cv2.VideoCapture(0) #0 or -1

while cap.isOpened():
    ret, img = cap.read()
    img = cv2.rotate(img, cv2.ROTATE_180)
    if ret:
        image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        detector = apriltag(tagFamily)
        detections = detector.detect(image)
        print("[INFO] {} total AprilTags detected".format(len(detections)))

        # loop over the AprilTag detection results
        for r in detections:
            # extract the bounding box (x, y)-coordinates for the AprilTag
            # and convert each of the (x, y)-coordinate pairs to integers
            (ptA, ptB, ptC, ptD) = r['lb-rb-rt-lt']
            ptB = (int(ptB[0]), int(ptB[1]))
            ptC = (int(ptC[0]), int(ptC[1]))
            ptD = (int(ptD[0]), int(ptD[1]))
            ptA = (int(ptA[0]), int(ptA[1]))

            # draw the bounding box of the AprilTag detection
            cv2.line(img, ptA, ptB, (0, 255, 0), 2)
            cv2.line(img, ptB, ptC, (0, 255, 0), 2)
            cv2.line(img, ptC, ptD, (0, 255, 0), 2)
            cv2.line(img, ptD, ptA, (0, 255, 0), 2)

            # draw the center (x, y)-coordinates of the AprilTag
            (cX, cY) = (int(r['center'][0]), int(r['center'][1]))
            cv2.circle(img, (cX, cY), 5, (0, 0, 255), -1)

            # draw the tag family on the image
            cv2.putText(img, tagFamily, (ptA[0], ptA[1] - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            print("[INFO] tag family: {}".format(tagFamily))

        cv2.imshow('camera', img)
        cv2.waitKey(1)
    else:
        print('no camera!')
        break
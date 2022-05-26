import cv2
import numpy as np


cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)
min = (7, 128, 76)
max = (30, 230, 255)

h_min = np.array(min, np.uint8)
h_max = np.array(max, np.uint8)

flag, img = cap.read()
trajectory = []

while True:
    flag, img = cap.read()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv = cv2.medianBlur(hsv, 5)
    thresh = cv2.inRange(hsv, h_min, h_max)
    moments = cv2.moments(thresh, 1)
    dM01 = moments['m01']
    dM10 = moments['m10']
    dArea = moments['m00']
    if dArea > 1000:
        x = int(dM10 / dArea)
        y = int(dM01 / dArea)
        cv2.circle(img, (x,y), 10, (255, 0, 0), -1)
        #print(f"x: {x}, y: {y}")
        coordinates = []
        coordinates.append(x)
        coordinates.append(y)
        if coordinates not in trajectory:
            trajectory.append(coordinates)
            for i in trajectory:
                cv2.circle(img, (i[0], i[1]), 5, (0, 0, 255), -1)
    cv2.imshow('result', img) 
    cv2.imshow('thresh', thresh)
    ch = cv2.waitKey(5)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


#print(trajectory)
cap.release()
cv2.destroyAllWindows()
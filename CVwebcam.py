import numpy as np
import cv2
from numpy.core.fromnumeric import resize

def nothing(x):
    pass

cap = cv2.VideoCapture(0)
cv2.namedWindow('Trackbars')
cv2.resizeWindow('Trackbars',500, 500)

cv2.createTrackbar('Thresh1', 'Trackbars', 150, 255, nothing)
cv2.createTrackbar('Thresh2', 'Trackbars', 255, 255, nothing)
cv2.createTrackbar('L - H', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('L - S', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('L - V', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('U - H', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('U - S', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('U - V', 'Trackbars', 255, 255, nothing)

def stackImg(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvaliable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvaliable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2:
                    imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3),np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver

def getContours(img, imgContour):
    contours,hierachy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x_dot = 0
    y_dot = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:
            # cv2.drawContours(frame, contour, -1, (0, 255, 0), 7)
            x,y,w,h = cv2.boundingRect(contour)
            x_dot = x+int((1/2)*w)
            y_dot = y+int((1/2*h))
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),5)
            cv2.circle(frame, (x_dot, y_dot), radius=5, color=(0,0,255),thickness=-1)
    if len(contours) == 1:
        return x_dot, y_dot
    else:
        return 0,0

def countContours(img, imgContour):
    contours,hierachy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return len(contours)


while True:
    ret, frame = cap.read()
    imgContour = frame.copy()

    imgBlur = cv2.GaussianBlur(frame, (7, 7), 1)
    imgHSV = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2HSV)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
    
    t1 = cv2.getTrackbarPos('Thresh1', 'Trackbars')
    t2 = cv2.getTrackbarPos('Thresh2', 'Trackbars')

    imgCanny = cv2.Canny(imgGray, t1, t2)

    l_h = cv2.getTrackbarPos('L - H', 'Trackbars')
    l_s = cv2.getTrackbarPos('L - S', 'Trackbars')
    l_v = cv2.getTrackbarPos('L - V', 'Trackbars')
    u_h = cv2.getTrackbarPos('U - H', 'Trackbars')
    u_s = cv2.getTrackbarPos('u - s', 'Trackbars')
    u_v = cv2.getTrackbarPos('U - V', 'Trackbars')

    lower = np.array([l_h, l_s, l_v], dtype=np.uint8)
    upper = np.array([u_h, u_s, u_v], dtype=np.uint8)
    imgMask = cv2.inRange(imgHSV, lower, upper)


   
    kernal = np.ones((5, 5))
    imgDil = cv2.dilate(imgCanny, kernal, iterations=1)
    
    contoursNum = countContours(imgDil, imgContour)
    if contoursNum == 0:
        x_pos, y_pos = getContours(imgMask, imgContour)
    else:
        x_pos, y_pos = getContours(imgDil, imgContour)
    
    print(x_pos, y_pos)
    

    imgStack = stackImg(0.8,([frame, imgCanny,imgDil],[imgMask, imgMask, imgMask]))
    # cv2.imshow('canny',imgCanny)
    cv2.imshow('all',imgStack)

    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
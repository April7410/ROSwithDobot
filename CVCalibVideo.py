# Import required modules
import cv2
import numpy as np
#import glob
#import os

# Define the dimensions of checkerboard
CHECKERBOARD = (5, 6)
FrameSize = (640, 480)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objPoints = []    # Vector for 3D points
imgPoints = []   # Vector for 2D points

# 3D points real world coordinates
objectp3d = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objectp3d[0, :, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
prev_img_shape = None

#vid = cv2.VideoCapture('/dev/video0')
vid = cv2.VideoCapture(0)
picTaken=3
counter=0
imagelist=[]
while counter<=picTaken:  #takes 4 pics
    ret, image = vid.read()
    cv2.imshow('VideoSteaming', image)
    
    #cv2.waitKey(0) #shoot photo
    #image = cv2.imread(pic)
    grayColor = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Find the chess board corners
    # If desired number of corners are found in the image then ret = true
    ret, corners = cv2.findChessboardCorners(
                    grayColor, CHECKERBOARD,
                    cv2.CALIB_CB_ADAPTIVE_THRESH
                    + cv2.CALIB_CB_FAST_CHECK +
                    cv2.CALIB_CB_NORMALIZE_IMAGE)
    print(ret,corners)
    if ret==True: 	# return of cv2.findChessboardCorners==True
        objPoints.append(objectp3d)
        # Refining pixel coordinates for given 2d points.
        corners2 = cv2.cornerSubPix(grayColor, corners, (11, 11), (-1, -1), criteria)
        #print(len(corners2))
        imgPoints.append(corners2)

        # Draw and display the corners
        # image = cv2.drawChessboardCorners(image, CHECKERBOARD, corners2, ret)
        imagelist.append(cv2.drawChessboardCorners(image, CHECKERBOARD, corners2, ret))
        counter += 1
        
        # cv2.imshow('ChessFoundImage{}'.format(counter), image)
        # #cv2.imwrite('Chess5x6Img{}'.format(counter), image)
        # cv2.waitKey(1000)

    #cv2.imwrite('chess5x6.png', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
for i in range(len(imagelist)):
    cv2.imshow('ChessFoundImage{}'.format(i), imagelist[i])
    #cv2.imwrite('Chess5x6Img{}'.format(counter), image)
    cv2.waitKey(1000)
cv2.waitKey(0)
#cv2.destroyAllWindows()
vid.release()
#h, w = image.shape[:2]

# Perform camera calibration by
# passing the value of above found out 3D points (threedpoints)
# and its corresponding pixel coordinates of the
# detected corners (twodpoints)
retval, CamMatrix, distortion, r_vecs, t_vecs = cv2.calibrateCamera(objPoints, imgPoints, FrameSize, None, None)

print(" Camera matrix:\n", CamMatrix)

print("\n Distortion coefficient:\n", distortion)

print("\n Rotation Vectors:\n", r_vecs)

print("\n Translation Vectors:\n", t_vecs)

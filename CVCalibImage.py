# Import required modules
import cv2
import numpy as np
import glob
#import os

# Define the dimensions of checkerboard
CHECKERBOARD = (5, 6)   # subject to change
FrameSize = (640, 480)  # or later use the "grayColor.shape[::-1]" instead

# stop the iteration when specified accuracy, epsilon, is reached 
# or specified number of iterations are completed.
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane

# 3D points real world coordinates
objectp3d = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objectp3d[0, :, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
prev_img_shape = None

# prepare all the .png to calibrate before executing this line
images = glob.glob('*.png') # Takes all current directory png files
ReturnList = []

for pic in images:
	print(pic)
	image = cv2.imread(pic)
	grayColor = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# Find the chess board corners
	# If desired number of corners are found in the image then ret = true
	ret, corners = cv2.findChessboardCorners(
					grayColor, CHECKERBOARD,
					cv2.CALIB_CB_ADAPTIVE_THRESH
					+ cv2.CALIB_CB_FAST_CHECK +
					cv2.CALIB_CB_NORMALIZE_IMAGE)
	print(ret)
	ReturnList.append(ret)
	# If desired number of corners can be detected then,
	# refine the pixel coordinates and display
	# them on the images of checkerboard
	if ret: 	# return of cv2.findChessboardCorners==True
		objpoints.append(objectp3d)
		# Refining pixel coordinates for given 2d points.
		corners2 = cv2.cornerSubPix(grayColor, corners, (11, 11), (-1, -1), criteria)
		#print(len(corners2))
		imgpoints.append(corners2)

		# Draw and display the corners
		image = cv2.drawChessboardCorners(image, CHECKERBOARD, corners2, ret)
		cv2.imshow('ChessFoundImage', image)
		cv2.waitKey(0)
	else:
		cv2.imshow('ChessNotFoundImage', image)
		cv2.waitKey(500)

cv2.destroyAllWindows()

h, w = image.shape[:2]

# Perform camera calibration by
# passing the value of above found out 3D points (threedpoints)
# and its corresponding pixel coordinates of the
# detected corners (twodpoints)
retval, CamMatrix, distortion, r_vecs, t_vecs = cv2.calibrateCamera(
	objpoints, imgpoints, FrameSize, None, None)
	#objpoints, imgpoints, grayColor.shape[::-1], None, None)
#print(grayColor.shape[::-1])
print("test what it lookslike\n", cv2.calibrateCamera(objpoints, imgpoints, FrameSize, None, None))

# Displaying required output
print(" Calibrated pic: ", ReturnList)

print(" Camera matrix:\n", CamMatrix)

print("\n Distortion coefficient:\n", distortion)

print("\n Rotation Vectors:\n", r_vecs)

print("\n Translation Vectors:\n", t_vecs)

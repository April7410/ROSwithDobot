# import the opencv library
import cv2
import apriltag
#import cvzone
#from cvzone.HandTrackingModule import HandDetector
# define a video capture object
# cap = cv2.VideoCapture("/dev/video0")
# cap = cv2.VideoCapture(0)

# while(True):
#     success, image = cap.read()
#     print(success)
#     # cv2.waitKey(0)
#     cv2.imshow('frame', image)
#     #cv2.imshow('frame',cap.read()[1])
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# img=cv2.imwrite('to_detectApril.png', image)
#image=cv2.imread("images/red.jpeg")        #read in image

image='to_detectApril.png'
img = cv2.imread(image.cv2.IMREAD_GRAYSCALE)
detector = apriltag.Detector()
result = detector.detect(img)
tf = result[0].tag_family
cx = result[0].center[0]

cv2.imshow("Image", image)
# After the loop release the cap object
cap.release()
# Destroy all the windows
cv2.destroyAllWindows()

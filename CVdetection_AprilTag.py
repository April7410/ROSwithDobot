# import the opencv library
import cv2
import apriltag
#import cvzone
#from cvzone.HandTrackingModule import HandDetector
# define a video capture object
cap = cv2.VideoCapture("/dev/video2")
# cap = cv2.VideoCapture(0)

while(True):
    success, image = cap.read()
    #print(success)
    # cv2.waitKey(0)
    cv2.imshow('frame', image)
    #cv2.imshow('frame',cap.read()[1])
    # img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # detector = apriltag.Detector()
    # result = detector.detect(img)
    # print(result)
    # tf = result[0].tag_family
    # cx = result[0].center[:]
    # print("Tag family is\t",tf)
    # print("Center of Tag is at\t", cx)
    # cv2.imshow("Image", image)
    #cv2.waitKey(0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
#image = cv2.imwrite('to_detectApril3.png', image)

# image = cv2.imread('to_detectApril.png')
# image = cv2.imread('to_detectApril2.png')
img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# img = cv2.IMREAD_GRAYSCALE
detector = apriltag.Detector()
result = detector.detect(img)
tf = result[0].tag_family
cx = result[0].center[:]
print("Tag family is\n",tf)
print("Center of Tag is at\n", cx)
cv2.imshow("Tag Detected Image", image)
cv2.waitKey(1)
# After the loop release the cap object
# cap.release()
# Destroy all the windows
cv2.destroyAllWindows()

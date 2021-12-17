# import the opencv library
import cv2
  
vid = cv2.VideoCapture("/dev/video2")
#vid = cv2.VideoCapture(0)
while(True):
    ret, frame = vid.read()
    cv2.imshow('frame', frame)  # Streaming
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.imwrite('NewPhoto.png', frame)
vid.release()
cv2.destroyAllWindows()

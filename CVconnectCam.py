# import the opencv library
# pip3 install opencv-python
import cv2

# vid = cv2.VideoCapture(0)  # define a video capture object
vid = cv2.VideoCapture("/dev/video2") # find the non-default external camera port
while(True):
    ret, frame = vid.read()      # Capture the video frame
    cv2.imshow('frame', frame)   # steams images into video
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break    # the 'q' button is set as the quitting button

vid.release()    # After the loop release the cap object
cv2.destroyAllWindows()          # Destroy all the windows

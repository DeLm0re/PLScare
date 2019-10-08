import tensorflow as tf
import numpy as np
from scipy.fftpack import fft
import cv2
import matplotlib.pyplot as plt

import skinMask


# Captured frames counter
capturedFrames = 0
# Output videos names
videoName = 'originalVideo.avi'


print('Starting capture')
cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
videoOut = cv2.VideoWriter(videoName,fourcc, 60.0, (640,480))


while cap.isOpened():
    # Check video aquisition
    ret, frame = cap.read()
    if ret:

        capturedFrames = capturedFrames + 1

        # flip the frame to be mirror like
        frame = cv2.flip(frame,1)

        # get average HSV frame and skin detection frame
        hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        skin = skinMask.getSkin(frame, hsvFrame)


        # show the skin in the image along with the mask
        cv2.imshow('frame', np.hstack([frame, skin]))

        # ignore the 100 first frames
        if capturedFrames >= 100:
            # Write frame
            videoOut.write(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    else:
        break

# Release everything if job is finished
cap.release()
videoOut.release()
cv2.destroyAllWindows()

print('End of recording')

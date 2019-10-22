import tensorflow as tf
import numpy as np
from scipy.fftpack import fft
import cv2
import matplotlib.pyplot as plt

import skinMask


# Output videos name
videoName = 'originalVideo.avi'


print('Starting capture')
cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
videoOut = cv2.VideoWriter(videoName,fourcc, 30, (640,480))

recordedFrame = 0

while cap.isOpened():
    # Check video aquisition
    ret, frame = cap.read()
    if ret:

        # flip the frame to be mirror like
        frame = cv2.flip(frame,1)

        # get average HSV frame and skin detection frame
        hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        skin = skinMask.getSkin(frame, hsvFrame)

        x = 300
        y = 150
        w = 100
        h = 50
        roi = frame[y:y + h, x:x + w]
        hsvRoi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        s = skinMask.getSkin(roi, hsvRoi)
        cv2.imshow('frame', np.hstack([roi, s]))

        # show the skin in the image along with the mask
        #cv2.imshow('frame', np.hstack([frame, skin]))

        # Write frame
        if recordedFrame > 50 :
            videoOut.write(frame)

        recordedFrame = recordedFrame + 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    else:
        break

# Release everything if job is finished
cap.release()
videoOut.release()
cv2.destroyAllWindows()

print('End of recording')

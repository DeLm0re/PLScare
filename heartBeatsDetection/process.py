import numpy as np
from scipy.fftpack import fft
import cv2
import matplotlib.pyplot as plt

import skinMask


# List of average hue for each frame
meanHues = []
# Number of recorded frames
recordedFrames = 0
# Output videos names
videoName = 'originalVideo.avi'
skinName = 'skinMask.avi'


print('Processing...')
cap = cv2.VideoCapture(videoName)

while cap.isOpened():
    # Check video aquisition
    ret, frame = cap.read()
    if ret:

        # get average HSV frame and skin detection frame
        #frame = cv2.fastNlMeansDenoisingColored(frame, None, 10, 10, 7, 21)
        hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        skin = skinMask.getSkin(frame, hsvFrame)

        # get average Hue value for the pixels of skin
        hues = skin[:, :, 0]

        # show the skin in the image along with the mask
        cv2.imshow('frame', np.hstack([frame, skin]))

        # Save the average hues
        meanHues.append(np.mean(hues))

        recordedFrames = recordedFrames + 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    else:
        break

# Release everything if job is finished
cap.release()
cv2.destroyAllWindows()


plt.plot(meanHues)
plt.title("Average Hues per frame")
plt.ylabel("Average Hue")
plt.xlabel("Frame number")
plt.show()


x = range(1, recordedFrames + 1)
y = meanHues

yf = fft(y)

plt.plot(x, yf)
plt.title("FFT")
plt.xlabel("Frame number")
plt.show()

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

# Find OpenCV version
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
if int(major_ver) < 3:
    fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
else:
    fps = cap.get(cv2.CAP_PROP_FPS)


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

N = recordedFrames
T = 1.0/fps
f = 1.0/(2.0*T)

x = np.linspace(0.0, N*T, N)
y = np.diff(meanHues)/np.diff(x)
x = x[:-1]

plt.plot(x, y)
plt.title("Average Hues per frame")
plt.ylabel("Average Hue")
plt.xlabel("Time (s)")
plt.show()

xf = np.linspace(0.0, f, N//2)
xf = xf[:-1]
yf = fft(y)
yf = yf[N//2:N//2 + len(xf)]

plt.plot(xf, yf)
plt.title("FFT")
plt.xlabel("Hz")
plt.show()

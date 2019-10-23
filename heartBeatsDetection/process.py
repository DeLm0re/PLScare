import numpy as np
from scipy.fftpack import fft
import cv2
import matplotlib.pyplot as plt

import RGBtoHSV

# List of average hue for each frame
meanHues = []
# Number of recorded frames
recordedFrames = 0
# Output videos names
videoName = 'originalVideo.avi'

print('Processing...')
cap = cv2.VideoCapture(videoName)

# Find OpenCV version
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
# Get frame per seconds
if int(major_ver) < 3:
    fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
else:
    fps = cap.get(cv2.CAP_PROP_FPS)


while cap.isOpened():
    # Check video aquisition
    ret, frame = cap.read()
    if ret:

        # Temporary Region Of Interest to target forehead
        x = 300
        y = 150
        w = 100
        h = 50
        roi = frame[y:y + h, x:x + w]

        #roi = cv2.fastNlMeansDenoisingColored(roi, None, 10, 10, 7, 21)
        #hsvRoi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        [hues, _, _] = RGBtoHSV.RGBimageToHSV(roi)

        cv2.imshow('frame', roi)

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

# Plot data
N = recordedFrames
T = 1.0/fps
f = 1.0/(2.0*T)

x = np.linspace(0.0, N*T, N)
y = meanHues

plt.plot(x, y)
plt.title("Average Hues per frame")
plt.ylabel("Average Hue")
plt.xlabel("Time (s)")
plt.show()

xf = np.linspace(0.0, f, N//2)
xf = xf[:-1]
yf = fft(y)
yf = yf[N//2:N//2 + len(xf)]

# Band-pass filter to the interesting frequencies
HRindex = (xf >= 0.2) & (xf <= 4.0)

plt.plot(xf[HRindex], yf[HRindex])
plt.title("FFT")
plt.xlabel("Hz")
plt.show()

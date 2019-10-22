import cv2
import numpy as np

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

        # temporary Region Of Interest to target forehead
        x = 300
        y = 150
        w = 100
        h = 50
        roi = frame[y:y + h, x:x + w]

        # show the captured frame along with the ROI
        showedFrame = np.copy(frame)
        cv2.rectangle(showedFrame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.imshow('frame', showedFrame)


        # Write frame
        if recordedFrame > 50:
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

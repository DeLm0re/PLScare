import numpy as np
import cv2


def start_recording(videoName, cam_id):

    videoName = videoName + '.avi'

    # Create a capture object wired on the default webcam (cam_id)
    cap = cv2.VideoCapture(cam_id)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    videoOut = cv2.VideoWriter(videoName, fourcc, 30, (640,480))


    print('Starting capture')
    while cap.isOpened():
        # Check video aquisition
        ret, frame = cap.read()
        if ret:

            # flip the frame to be mirror like
            frame = cv2.flip(frame,1)

            # show the captured image
            cv2.imshow('frame', frame)

            # Write frame
            videoOut.write(frame)

            # Get keyboard input
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        else:
            break

    # Release everything when the job is finished
    cap.release()
    videoOut.release()
    cv2.destroyAllWindows()

    print('End of recording')
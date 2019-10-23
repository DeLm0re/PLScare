# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2
import math


def get_person_detection(frame, net):

    # grab the frame dimensions and convert it to a blob
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

    # pass the blob through the network and obtain the detections and
    # predictions
    net.setInput(blob)
    detections = net.forward()
    return detections


def handle_person_detection(frame, detections):
    (frame_height, frame_width) = frame.shape[:2]
    distance_min = 1000000
    index_min = -1

    # loop over the detections
    for i in np.arange(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with
        # the prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the `confidence` is
        # greater than the minimum confidence
        if confidence > 0.2:
            # extract the index of the class label from the
            # `detections`, then compute the (x, y)-coordinates of
            # the bounding box for the object
            idx = int(detections[0, 0, i, 1])

            if idx == 15:
                box = detections[0, 0, i, 3:7] * np.array([frame_width, frame_height, frame_width, frame_height])
                (start_x, start_y, end_x, end_y) = box.astype("int")

                x_avg = (start_x + end_x) / 2
                y_avg = (start_y + end_y) / 2

                distance = math.sqrt(math.pow((x_avg - 150), 2) + math.pow((y_avg - 150), 2))

                if distance < distance_min:
                    distance_min = distance
                    index_min = i

    if not index_min == -1:
        box = detections[0, 0, index_min, 3:7] * np.array([frame_width, frame_height, frame_width, frame_height])
        (start_x, start_y, end_x, end_y) = box.astype("int")
        cropped_frame = frame[start_y: end_y, start_x: end_x]
        cropped_frame_height, cropped_frame_width = cropped_frame.shape[:2]
        if cropped_frame_height == 0 or cropped_frame_width == 0:
            cropped_frame = frame

    return cropped_frame


def main_person_detection(py_args):
    # load our serialized model from disk
    print("[INFO] loading model...")
    net = cv2.dnn.readNetFromCaffe(py_args["prototxt"], py_args["model"])

    # initialize the video stream, allow the camera sensor to warm-up,
    # and initialize the FPS counter
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    fps = FPS().start()

    while True:
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        frame = vs.read()
        frame = imutils.resize(frame, width=400)

        detections = get_person_detection(frame, net)
        person_detected_nb = sum(1 for element in (detections[0, 0, :, 1] == 15) if (element == True))

        if person_detected_nb == 0:
            frame = np.rot90(frame)
            detections = get_person_detection(frame, net)
            person_detected_nb = sum(1 for element in (detections[0, 0, :, 1] == 15) if (element is True))

            if person_detected_nb == 0:
                frame = np.rot90(frame,2)
                detections = get_person_detection(frame, net)
                person_detected_nb = sum(1 for element in (detections[0, 0, :, 1] == 15) if (element is True))

        if not person_detected_nb == 0:
            frame = handle_person_detection(frame, detections)

        # show the output frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

        # update the FPS counter
        fps.update()

    # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()

    return 0


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True,
                help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
                help="path to Caffe pre-trained model")
args = vars(ap.parse_args())

main_person_detection(args)
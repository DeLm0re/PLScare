# import the necessary packages
import numpy as np
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


def person_detection_module(cap, video_output):
    # load our serialized model from disk
    net = cv2.dnn.readNetFromCaffe("custom/assets/caffe_models/MobileNetSSD_deploy.prototxt.txt",
                                   "custom/assets/caffe_models/MobileNetSSD_deploy.caffemodel")

    frame_count = 0
    total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    laying_on_ground = .0

    while frame_count < total_frame:
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        res, frame = cap.read()
        if not res:
            raise IOError("video failure")

        detections = get_person_detection(frame, net)
        person_detected_nb = sum(1 for element in (detections[0, 0, :, 1] == 15) if (element == True))

        if person_detected_nb == 0:
            frame = np.rot90(frame)
            detections = get_person_detection(frame, net)
            person_detected_nb = sum(1 for element in (detections[0, 0, :, 1] == 15) if (element is True))

            if person_detected_nb == 0:
                frame = np.rot90(frame, 2)
                detections = get_person_detection(frame, net)
                person_detected_nb = sum(1 for element in (detections[0, 0, :, 1] == 15) if (element is True))

            laying_on_ground += 1

        if not person_detected_nb == 0:
            frame = handle_person_detection(frame, detections)

        video_output.append(frame)
        frame_count += 1
	
    return laying_on_ground/frame_count

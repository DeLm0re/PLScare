import tensorflow as tf
import cv2
import posenet
import time
import argparse
import matplotlib.pyplot as plt
import scipy.fftpack as fft
import numpy as np

import custom

parser = argparse.ArgumentParser()
parser.add_argument('--model', type=int, default=101)
parser.add_argument('--cam_id', type=int, default=0)
parser.add_argument('--cam_width', type=int, default=1280)
parser.add_argument('--cam_height', type=int, default=720)
parser.add_argument('--scale_factor', type=float, default=0.7125)
parser.add_argument('--file', type=str, default=None, help="Optionally use a video file instead of a live camera")
args = parser.parse_args()


def main():
    with tf.Session() as sess:
        # Use the video given as an argument or record one
        if args.file is not None:
            cap = cv2.VideoCapture(args.file)
        else:
            custom.video_acquisition.start_recording("video/video0", args.cam_id)
            cap = cv2.VideoCapture("video/video0.avi")
        # video parameter
        cap.set(3, args.cam_width)
        cap.set(4, args.cam_height)

        # frame and time information
        start = time.time()

        # diagnostic init
        symptoms = custom.detection.create_symptoms_dict()

        # --- Do coco treatment here
        # Get if the subject is laying on the floor and rotate the video if necessary to get better treatment results
        # (most treatment works only on standing up person)

        custom.wrapper.posenet_module(args, sess, cap, symptoms)

        cap.release()
        cv2.destroyAllWindows()
        custom.run_app()


if __name__ == "__main__":
    main()

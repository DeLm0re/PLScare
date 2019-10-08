import tensorflow as tf
import cv2
import posenet
import time
import argparse
import matplotlib.pyplot as plt
import scipy.fftpack as fft
import numpy as np

import PLScare

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
        # posenet init
        model_cfg, model_outputs = posenet.load_model(args.model, sess)
        output_stride = model_cfg['output_stride']

        # video init
        if args.file is not None:
            cap = cv2.VideoCapture(args.file)
        else:
            cap = cv2.VideoCapture(args.cam_id)
        cap.set(3, args.cam_width)
        cap.set(4, args.cam_height)

        # frame and time information
        start = time.time()
        frame_count = 0

        # array used for measurement
        time_array = []
        average_array = []

        # main loop
        while True:
            # read an image from the capture device or video
            input_image, display_image, output_scale = posenet.read_cap(
                cap, scale_factor=args.scale_factor, output_stride=output_stride)

            # extract info from image
            heatmaps_result, offsets_result, displacement_fwd_result, displacement_bwd_result = sess.run(
                model_outputs,
                feed_dict={'image:0': input_image}
            )

            # calculate the different points
            pose_scores, keypoint_scores, keypoint_coords = posenet.decode_multi.decode_multiple_poses(
                heatmaps_result.squeeze(axis=0),
                offsets_result.squeeze(axis=0),
                displacement_fwd_result.squeeze(axis=0),
                displacement_bwd_result.squeeze(axis=0),
                output_stride=output_stride,
                max_pose_detections=10,
                min_pose_score=0.15)

            keypoint_coords *= output_scale
            # show the points which has been found on the image
            overlay_image = posenet.draw_skel_and_kp(
                display_image, pose_scores, keypoint_scores, keypoint_coords,
                min_pose_score=0.15, min_part_score=0.1)

            # get the body on the image
            body_image = PLScare.detection.get_body(
                pose_scores,
                keypoint_scores,
                keypoint_coords,
                display_image)

            time_array.append(time.time() - start)
            average_array.append(PLScare.image_treatment.get_average_value(body_image))

            cv2.imshow("posenet", body_image)

            frame_count += 1

            # check the 'q' key to end th eloop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        plt.plot(time_array, average_array)
        plt.title("average over time")
        plt.xlabel("time (s)")
        plt.ylabel("average")
        plt.show()

        average_array_transform = fft.fft(average_array)
        nb_frequency = 500
        frequency_array = np.linspace(0, len(average_array_transform)/nb_frequency, len(average_array_transform))
        plt.plot(frequency_array, average_array_transform)
        plt.title("average over frequency")
        plt.xlabel("frequency")
        plt.ylabel("average")
        plt.show()

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

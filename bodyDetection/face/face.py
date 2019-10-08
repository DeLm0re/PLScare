import cv2
import posenet
import math


def get_eyes(pose_scores, keypoint_scores, keypoint_coords, img):
    cropped_img = img
    if len(pose_scores) > 0:
        # Get the skeleton with the highest score
        pose_id = 0
        pose_score = 0
        for pi in range(0, len(pose_scores)):
            if pose_scores[pi] > pose_score:
                pose_id = pi
                pose_score = pose_scores[pi]

        # Get the coordinate that describe the torso (y, x)
        left_ear_info = [0, 0]
        right_ear_info = [0, 0]
        left_eye_info = [0, 0]
        right_eye_info = [0, 0]
        for ki, (score, coord) in enumerate(zip(keypoint_scores[pose_id, :], keypoint_coords[pose_id, :, :])):
            if posenet.PART_NAMES[ki] == "leftEar":
                left_ear_info = coord
            if posenet.PART_NAMES[ki] == "rightEar":
                right_ear_info = coord
            if posenet.PART_NAMES[ki] == "leftEye":
                left_eye_info = coord
            if posenet.PART_NAMES[ki] == "rightEye":
                right_eye_info = coord

        # Get face proportion
        distance_eyes = left_eye_info[1] - right_eye_info[1]
        gold_height_face = math.pi * distance_eyes

        # Get coord and create the face square
        xmin = right_ear_info[1]
        xmax = left_ear_info[1]
        ymin = left_eye_info[0] - gold_height_face / 2
        ymax = left_eye_info[0] + gold_height_face / 2
        crop_square = [int(xmin),
                       int(ymin),
                       int(xmax - xmin),
                       int(ymax - ymin)]

        # Crop the image only if the square is valid and return it
        if crop_square[2] > 0 and crop_square[3] > 0:
            cropped_img = img[
                          crop_square[1]: crop_square[1] + crop_square[3],
                          crop_square[0]: crop_square[0] + crop_square[2]]
    return cropped_img

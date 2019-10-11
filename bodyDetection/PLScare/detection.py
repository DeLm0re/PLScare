import posenet
import math
import numpy as np


# Get the coordinates of the given body parts
def get_coord_skeleton(pose_id, keypoint_scores, keypoint_coords, parts_names):
    parts_coord = np.zeros((len(parts_names),2))

    for ki, (score, coord) in enumerate(zip(keypoint_scores[pose_id, :], keypoint_coords[pose_id, :, :])):
        for index, part_name in enumerate(parts_names):
            if posenet.PART_NAMES[ki] == part_name:
                parts_coord[index] = coord
    return parts_coord


# Create a square out of the different coordinate
def create_square(xmin, xmax, ymin, ymax, scale):
    square = [int(xmin),
              int(ymin),
              int(xmax - xmin),
              int(ymax - ymin)]
    square[0] -= int((square[2] * scale - square[2]) / 2)
    square[1] -= int((square[3] * scale - square[3]) / 2)
    square[2] = int(square[2] * scale)
    square[3] = int(square[3] * scale)

    return square


# Create and crop the image only if the square is valid
def create_image(square, image):
    cropped_image = image
    if square[2] > 0 and square[3] > 0:
        cropped_image = image[
                        square[1]: square[1] + square[3],
                        square[0]: square[0] + square[2]]

    return cropped_image


def get_height_face(x_left_eye, x_right_eye):
    distance_eyes = x_left_eye - x_right_eye
    height_face = math.pi * distance_eyes

    return height_face


def get_body(pose_scores, keypoint_scores, keypoint_coords, image):
    if len(pose_scores) > 0:
        pose_id = np.argmax(pose_scores)
        parts_names = ['leftShoulder', 'rightShoulder', 'leftHip', 'rightHip']

        left_shoulder_info, right_shoulder_info, left_hip_info, right_hip_info = \
            get_coord_skeleton(pose_id, keypoint_scores, keypoint_coords,parts_names)

        xmin = min(left_shoulder_info[1], right_shoulder_info[1], left_hip_info[1], right_hip_info[1])
        xmax = max(left_shoulder_info[1], right_shoulder_info[1], left_hip_info[1], right_hip_info[1])
        ymin = min(left_shoulder_info[0], right_shoulder_info[0], left_hip_info[0], right_hip_info[0])
        ymax = max(left_shoulder_info[0], right_shoulder_info[0], left_hip_info[0], right_hip_info[0])

        square = create_square(xmin, xmax, ymin, ymax, 1.3)

        return create_image(square, image)


def get_face(pose_scores, keypoint_scores, keypoint_coords, image):
    if len(pose_scores) > 0:
        pose_id = np.argmax(pose_scores)
        parts_names = ['leftEar', 'rightEar', 'leftEye', 'rightEye']

        left_ear_info, right_ear_info, left_eye_info, right_eye_info = \
            get_coord_skeleton(pose_id, keypoint_scores, keypoint_coords,parts_names)

        xmin = right_ear_info[1]
        xmax = left_ear_info[1]
        ymin = left_eye_info[0] - get_height_face(left_eye_info[1], right_eye_info[1]) / 2
        ymax = left_eye_info[0] + get_height_face(left_eye_info[1], right_eye_info[1]) / 2

        square = create_square(xmin, xmax, ymin, ymax, scale=1)

        return create_image(square, image)

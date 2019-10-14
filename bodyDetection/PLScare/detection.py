import posenet
import math
import numpy as np


# Get the coordinate that describe the torso
def get_coord_skeleton(pose_id, keypoint_scores, keypoint_coords, part_name):
    part_coord = [0, 0]
    part_score = 0
    for ki, (score, coord) in enumerate(zip(keypoint_scores[pose_id, :], keypoint_coords[pose_id, :, :])):
        if posenet.PART_NAMES[ki] == part_name:
            part_coord = coord
            part_score = score
    info = dict()
    info['x'] = part_coord[0]
    info['y'] = part_coord[1]
    info['score'] = part_score
    return info


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
def crop_image(square, image):
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

        left_shoulder_info = get_coord_skeleton(pose_id, keypoint_scores, keypoint_coords, 'leftShoulder')
        right_shoulder_info = get_coord_skeleton(pose_id, keypoint_scores, keypoint_coords, 'rightShoulder')
        left_hip_info = get_coord_skeleton(pose_id, keypoint_scores, keypoint_coords, 'leftHip')
        right_hip_info = get_coord_skeleton(pose_id, keypoint_scores, keypoint_coords, 'rightHip')

        x_min = min(left_shoulder_info['x'], right_shoulder_info['x'], left_hip_info['x'], right_hip_info['x'])
        x_max = max(left_shoulder_info['x'], right_shoulder_info['x'], left_hip_info['x'], right_hip_info['x'])
        y_min = min(left_shoulder_info['y'], right_shoulder_info['y'], left_hip_info['y'], right_hip_info['y'])
        y_max = max(left_shoulder_info['y'], right_shoulder_info['y'], left_hip_info['y'], right_hip_info['y'])

        square = create_square(x_min, x_max, y_min, y_max, 1.3)

        return crop_image(square, image)


def get_face(pose_scores, keypoint_scores, keypoint_coords, image):
    if len(pose_scores) > 0:
        pose_id = np.argmax(pose_scores)
        parts_names = ['leftEar', 'rightEar', 'leftEye', 'rightEye']

        left_ear_info = get_coord_skeleton(pose_id, keypoint_scores, keypoint_coords, 'leftEar')
        right_ear_info = get_coord_skeleton(pose_id, keypoint_scores, keypoint_coords, 'rightEar')
        left_eye_info = get_coord_skeleton(pose_id, keypoint_scores, keypoint_coords, 'leftEye')
        right_eye_info = get_coord_skeleton(pose_id, keypoint_scores, keypoint_coords, 'rightEye')

        x_min = right_ear_info['x']
        x_max = left_ear_info['x']
        y_min = left_eye_info['y'] - get_height_face(left_eye_info['x'], right_eye_info['x']) / 2
        y_max = left_eye_info['y'] + get_height_face(left_eye_info['x'], right_eye_info['x']) / 2

        square = create_square(x_min, x_max, y_min, y_max, scale=1)

        return crop_image(square, image)


def is_hand_near_throat(pose_scores, keypoint_scores, keypoint_coords):
    if len(pose_scores) > 0:
        # Extract all pose and information used for the detection
        pose_id = np.argmax(pose_scores)
        left_shoulder_info = \
            get_coord_skeleton(pose_id, keypoint_scores, keypoint_coords, 'leftShoulder')
        right_shoulder_info = \
            get_coord_skeleton(pose_id, keypoint_scores, keypoint_coords, 'rightShoulder')
        left_elbow_info = \
            get_coord_skeleton(pose_id, keypoint_scores, keypoint_coords, 'leftElbow')
        right_elbow_info = \
            get_coord_skeleton(pose_id, keypoint_scores, keypoint_coords, 'rightElbow')
        left_wrist_info = \
            get_coord_skeleton(pose_id, keypoint_scores, keypoint_coords, 'leftWrist')
        right_wrist_info = \
            get_coord_skeleton(pose_id, keypoint_scores, keypoint_coords, 'rightWrist')

        # get the best elbow and shoulder point
        if left_shoulder_info['score'] > right_shoulder_info['score']:
            y_shoulder = left_shoulder_info['y']
        else:
            y_shoulder = right_shoulder_info['y']

        if left_elbow_info['score'] > right_elbow_info['score']:
            y_elbow = left_elbow_info['y']
        else:
            y_elbow = right_elbow_info['y']

        # get the best valid wrist point
        if left_wrist_info['y'] < y_elbow and right_wrist_info['y'] < y_elbow:
            if left_wrist_info['score'] > right_wrist_info['score']:
                y_wrist = left_wrist_info['y']
            else:
                y_wrist = right_wrist_info['y']
        elif left_wrist_info['y'] < y_elbow:
            y_wrist = left_wrist_info['y']
        elif right_wrist_info['y'] < y_elbow:
            y_wrist = right_wrist_info['y']
        else:
            return False

        if np.abs(y_shoulder-y_wrist) > np.abs(y_elbow-y_wrist):
            return False

    return True

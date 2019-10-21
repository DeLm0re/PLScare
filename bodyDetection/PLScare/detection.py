import posenet
import math
import numpy as np


# Get the coordinate that describe the torso
def get_info_skeleton(pose_id, keypoint_scores, keypoint_coords, part_names):
    total_info = dict()
    for ki, (score, coord) in enumerate(zip(keypoint_scores[pose_id, :], keypoint_coords[pose_id, :, :])):
        for part_name in part_names:
            if posenet.PART_NAMES[ki] == part_name:
                total_info[part_name] = dict()
                total_info[part_name]['x'] = coord[1]
                total_info[part_name]['y'] = coord[0]
                total_info[part_name]['score'] = score
    return total_info


# Get the pose id of the skeleton which is the most centered on the picture
def get_pose_id_closest_to_center(keypoint_scores, keypoint_coords, window_height, window_width):
    nb_pose = len(keypoint_scores)
    list_center_gravity = [[0 for x in range(2)] for y in range(nb_pose)]
    for pose_id in range(nb_pose):
        for ki, (score, coord) in enumerate(zip(keypoint_scores[pose_id, :], keypoint_coords[pose_id, :, :])):
            list_center_gravity[pose_id][1] = np.average(coord[1])
            list_center_gravity[pose_id][0] = np.average(coord[0])

    x_center = window_width/2
    y_center = window_height/2
    list_dist_center = np.zeros(nb_pose)
    for pose_id in range(nb_pose):
        list_dist_center[pose_id] = \
            np.power(list_center_gravity[pose_id][1] - x_center, 2) + \
            np.power(list_center_gravity[pose_id][0] - y_center, 2)

    return np.argmin(list_dist_center)


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


def get_body(pose_id, keypoint_scores, keypoint_coords, image, window_width, window_height):
    if len(pose_id) > 0:
        parts_names = ['leftShoulder', 'rightShoulder', 'leftHip', 'rightHip']

        parts_info = get_info_skeleton(pose_id, keypoint_scores, keypoint_coords, parts_names)

        x_min = min(parts_info['leftShoulder']['x'], parts_info['rightShoulder']['x'],
                    parts_info['leftHip']['x'], parts_info['rightHip']['x'])
        x_max = max(parts_info['leftShoulder']['x'], parts_info['rightShoulder']['x'],
                    parts_info['leftHip']['x'], parts_info['rightHip']['x'])
        y_min = min(parts_info['leftShoulder']['y'], parts_info['rightShoulder']['y'],
                    parts_info['leftHip']['y'], parts_info['rightHip']['y'])
        y_max = max(parts_info['leftShoulder']['y'], parts_info['rightShoulder']['y'],
                    parts_info['leftHip']['y'], parts_info['rightHip']['y'])

        square = create_square(x_min, x_max, y_min, y_max, 1.3)

        return crop_image(square, image)


def get_face(pose_id, keypoint_scores, keypoint_coords, image):
    if len(pose_id) > 0:
        parts_names = ['leftEar', 'rightEar', 'leftEye', 'rightEye']

        parts_info = get_info_skeleton(pose_id, keypoint_scores, keypoint_coords, parts_names)

        x_min = parts_info['rightEar']['x']
        x_max = parts_info['leftEar']['x']
        y_min = parts_info['leftEye']['y']-get_height_face(parts_info['leftEye']['x'], parts_info['rightEye']['x']) / 2
        y_max = parts_info['leftEye']['y']+get_height_face(parts_info['leftEye']['x'], parts_info['rightEye']['x']) / 2

        square = create_square(x_min, x_max, y_min, y_max, scale=1)

        return crop_image(square, image)


def get_person(pose_id, keypoint_scores, keypoint_coords, image):
    if len(pose_id) > 0:
        parts_names = ['nose', 'leftEye', 'rightEye', 'leftEar', 'rightEar', 'leftShoulder', 'rightShoulder',
                       'leftElbow', 'rightElbow', 'leftWrist', 'rightWrist', 'leftHip', 'rightHip', 'leftKnee',
                       'rightKnee', 'leftAnkle', 'rightAnkle']

        parts_info = np.array(get_info_skeleton(pose_id, keypoint_scores, keypoint_coords, parts_names))

        x_min = min(parts_info[:]['x'])
        x_max = max(parts_info[:]['x'])
        y_min = min(parts_info[:]['y'])
        y_max = max(parts_info[:]['y'])

        square = create_square(x_min, x_max, y_min, y_max, scale=1)

        return crop_image(square, image)


def is_hand_near_throat(pose_id, keypoint_scores, keypoint_coords):
    if len(pose_id) > 0:
        # Extract all information used for the detection
        parts_names = ['leftShoulder', 'rightShoulder', 'leftElbow', 'rightElbow', 'leftWrist', 'rightWrist']
        parts_info = get_info_skeleton(pose_id, keypoint_scores, keypoint_coords, parts_names)

        # get the best elbow and shoulder point
        if parts_info['leftShoulder']['score'] > parts_info['rightShoulder']['score']:
            y_shoulder = parts_info['leftShoulder']['y']
        else:
            y_shoulder = parts_info['rightShoulder']['y']

        if parts_info['leftElbow']['score'] > parts_info['rightElbow']['score']:
            y_elbow = parts_info['leftElbow']['y']
        else:
            y_elbow = parts_info['rightElbow']['y']

        # get the best valid wrist point
        if parts_info['leftWrist']['y'] < y_elbow and parts_info['rightWrist']['y'] < y_elbow:
            if parts_info['leftWrist']['score'] > parts_info['rightWrist']['score']:
                y_wrist = parts_info['leftWrist']['y']
            else:
                y_wrist = parts_info['rightWrist']['y']
        elif parts_info['leftWrist']['y'] < y_elbow:
            y_wrist = parts_info['leftWrist']['y']
        elif parts_info['rightWrist']['y'] < y_elbow:
            y_wrist = parts_info['rightWrist']['y']
        else:
            return False

        if np.abs(y_shoulder-y_wrist) > np.abs(y_elbow-y_wrist):
            return False

    return True


def is_mouth_open_throat(pose_id, keypoint_scores, keypoint_coords):
    return False


def get_symptoms(pose_scores, keypoint_scores, keypoint_coords, image, window_height, window_width):
    symptoms = dict()
    pose_id = get_pose_id_closest_to_center(keypoint_scores, keypoint_coords, window_height, window_width)

    symptoms["hand_near_throat"] = is_hand_near_throat(pose_id, keypoint_scores, keypoint_coords)
    symptoms["eyes_close"] = False
    symptoms["mouth_open"] = False
    symptoms["laying_on_ground"] = False
    symptoms["fast_cardiac_pace"] = False
    return symptoms

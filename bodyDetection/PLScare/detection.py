import posenet
import math
import numpy as np
import cv2
import PLScare


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

    x_center = window_width / 2
    y_center = window_height / 2
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


# get the height of the face based on the eyes
def get_height_face(x_left_eye, x_right_eye):
    distance_eyes = x_left_eye - x_right_eye
    height_face = math.pi * distance_eyes

    return height_face


# Crop the body from a posenet skeleton
def get_body(pose_id, keypoint_scores, keypoint_coords, image):
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


# Crop the face from a posenet skeleton
def get_face(pose_id, keypoint_scores, keypoint_coords, image):
    parts_names = ['leftEar', 'rightEar', 'leftEye', 'rightEye']

    parts_info = get_info_skeleton(pose_id, keypoint_scores, keypoint_coords, parts_names)

    x_min = parts_info['rightEar']['x']
    x_max = parts_info['leftEar']['x']
    y_min = parts_info['leftEye']['y'] - get_height_face(parts_info['leftEye']['x'], parts_info['rightEye']['x']) / 2
    y_max = parts_info['leftEye']['y'] + get_height_face(parts_info['leftEye']['x'], parts_info['rightEye']['x']) / 2

    square = create_square(x_min, x_max, y_min, y_max, scale=1)

    return crop_image(square, image)


# Crop the forehead person from a posenet skeleton
def get_forehead(pose_id, keypoint_scores, keypoint_coords, image):
    parts_names = ['leftEye', 'rightEye']
    parts_info = get_info_skeleton(pose_id, keypoint_scores, keypoint_coords, parts_names)

    face_height = get_height_face(parts_info['leftEye']['x'], parts_info['rightEye']['x'])

    top_forehead = parts_info['leftEye']['y'] - face_height / 2
    bottom_forehead = max(parts_info['rightEye']['y'], parts_info['leftEye']['y'])
    y_min = top_forehead + abs(bottom_forehead - top_forehead)/2
    y_max = bottom_forehead - abs(bottom_forehead - top_forehead)/3
    x_min = parts_info['rightEye']['x']
    x_max = parts_info['leftEye']['x']
    square = create_square(x_min, x_max, y_min, y_max, scale=1)
    return crop_image(square, image)


# Crop the full person from a posenet skeleton
def get_person(pose_id, keypoint_scores, keypoint_coords, image):
    parts_names = ['nose', 'leftEye', 'rightEye', 'leftEar', 'rightEar', 'leftShoulder', 'rightShoulder',
                   'leftElbow', 'rightElbow', 'leftWrist', 'rightWrist', 'leftHip', 'rightHip', 'leftKnee',
                   'rightKnee', 'leftAnkle', 'rightAnkle']

    parts_info = get_info_skeleton(pose_id, keypoint_scores, keypoint_coords, parts_names)

    x_min = min(parts_info[:]['x'])
    x_max = max(parts_info[:]['x'])
    y_min = min(parts_info[:]['y'])
    y_max = max(parts_info[:]['y'])

    square = create_square(x_min, x_max, y_min, y_max, scale=1)

    return crop_image(square, image)


# Crop the full person from a posenet skeleton
def get_mouth(pose_id, keypoint_scores, keypoint_coords, image):
    parts_names = ['nose', 'leftEar', 'rightEar', 'leftEye', 'rightEye']
    parts_info = get_info_skeleton(pose_id, keypoint_scores, keypoint_coords, parts_names)

    y_max = parts_info['leftEye']['y'] + get_height_face(parts_info['leftEye']['x'], parts_info['rightEye']['x']) / 2
    y_min = parts_info['nose']['y'] + np.abs(y_max - parts_info['nose']['y']) / 2
    x_min = parts_info['rightEar']['x'] + np.abs(parts_info['leftEar']['x'] - parts_info['rightEar']['x']) / 3
    x_max = parts_info['leftEar']['x'] - np.abs(parts_info['leftEar']['x'] - parts_info['rightEar']['x']) / 3
    square = create_square(x_min, x_max, y_min, y_max, scale=1)
    return crop_image(square, image)


# Check if the hand is near the throat on a posenet skeleton
def is_hand_near_throat(pose_id, keypoint_scores, keypoint_coords):
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

    if np.abs(y_shoulder - y_wrist) > np.abs(y_elbow - y_wrist):
        return False

    return True


# Check if the mouth is open based on a posenet skeleton
def is_mouth_open(pose_id, keypoint_scores, keypoint_coords, image):
    image_mouth = get_mouth(pose_id, keypoint_scores, keypoint_coords, image)

    hsv = cv2.cvtColor(image_mouth, cv2.COLOR_BGR2HSV)
    average_value = np.average(hsv[:, :, 2])

    image_face = get_face(pose_id, keypoint_scores, keypoint_coords, image)
    base_value = PLScare.image_treatment.get_average_value(image_face)

    if np.abs(base_value - average_value) > 15:
        return True
    else:
        return False


# Create a dictionary of symptoms
def create_symptoms_dict():
    symptoms = dict()
    symptoms["hand_near_throat"] = 0.
    symptoms["eyes_close"] = 0.
    symptoms["mouth_open"] = 0.
    symptoms["laying_on_ground"] = 0.
    symptoms["fast_cardiac_pace"] = 0.
    symptoms["no_cardiac_pace"] = 0.
    return symptoms


# Get the diagnostic of a person based on his symptoms
# Each symptoms should be a percentage
def get_diagnostics(symptoms):
    diagnostic = dict()
    diagnostic["Etouffement"] = \
        (symptoms["hand_near_throat"] + symptoms["mouth_open"] + (1 - symptoms["eyes_close"]) +
         symptoms["fast_cardiac_pace"] + (1 - symptoms["laying_on_ground"])) / 5

    diagnostic["Inconscient"] = \
        (symptoms["eyes_close"] + symptoms["laying_on_ground"] +
         (1 - symptoms["fast_cardiac_pace"] + 1 - symptoms["no_cardiac_pace"])) / 5

    diagnostic["Arret_cardiaque"] = \
        ((1 - symptoms["eyes_close"]) + symptoms["laying_on_ground"] + symptoms["no_cardiac_pace"]) / 5

    # To differentiate these two, ask the user if the person is hurt
    diagnostic["Malaise_cardiaque"] = \
        ((1 - symptoms["eyes_close"]) + 1 + 1) / 5  # (+ 1 whatever position) (+ 1 whatever cardiac pace)

    diagnostic["Saignement"] = \
        ((1 - symptoms["eyes_close"]) + symptoms["fast_cardiac_pace"] + 1) / 5  # (+ 1 whatever position)

    return diagnostic

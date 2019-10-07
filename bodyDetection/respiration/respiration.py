import cv2
import posenet


def get_body(pose_scores, keypoint_scores, keypoint_coords, img):
    cropped_img = img
    if len(pose_scores) > 0:
        # Get the skeleton with the highest score
        pose_id = 0
        pose_score = 0
        for pi in range(0, len(pose_scores)):
            if pose_scores[pi] > pose_score:
                pose_id = pi
                pose_score = pose_scores[pi]

        # Get the coordinate that describe the torso
        left_shoulder_info = [0, 0]
        right_shoulder_info = [0, 0]
        left_hip_info = [0, 0]
        right_hip_info = [0, 0]
        for ki, (score, coord) in enumerate(zip(keypoint_scores[pose_id, :], keypoint_coords[pose_id, :, :])):
            if posenet.PART_NAMES[ki] == "leftShoulder":
                left_shoulder_info = coord
            if posenet.PART_NAMES[ki] == "rightShoulder":
                right_shoulder_info = coord
            if posenet.PART_NAMES[ki] == "leftHip":
                left_hip_info = coord
            if posenet.PART_NAMES[ki] == "rightHip":
                right_hip_info = coord

        # Create a square out of the different coordinate
        xmin = min(left_shoulder_info[1], right_shoulder_info[1], left_hip_info[1], right_hip_info[1])
        xmax = max(left_shoulder_info[1], right_shoulder_info[1], left_hip_info[1], right_hip_info[1])
        ymin = min(left_shoulder_info[0], right_shoulder_info[0], left_hip_info[0], right_hip_info[0])
        ymax = max(left_shoulder_info[0], right_shoulder_info[0], left_hip_info[0], right_hip_info[0])
        crop_square = [int(xmin),
                       int(ymin),
                       int(xmax-xmin),
                       int(ymax-ymin)]

        scale = 1.3
        crop_square[0] -= int((crop_square[2]*scale - crop_square[2])/2)
        crop_square[1] -= int((crop_square[3]*scale - crop_square[3])/2)
        crop_square[2] = int(crop_square[2]*scale)
        crop_square[3] = int(crop_square[3]*scale)

        # Crop the image only if the square is valid and return it
        if crop_square[2] > 0 and crop_square[3] > 0:
            cropped_img = img[
                          crop_square[1]: crop_square[1]+crop_square[3],
                          crop_square[0]: crop_square[0]+crop_square[2]]
    return cropped_img

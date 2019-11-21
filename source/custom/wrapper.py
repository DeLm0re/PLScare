import custom
import posenet
import cv2


def posenet_module(args, sess, video, symptoms):
    # Frame info
    frame_count = 0
    total_frame = len(video)

    # posenet init
    model_cfg, model_outputs = posenet.load_model(args.model, sess)
    output_stride = model_cfg['output_stride']
    # posenet treatment loop
    while frame_count < total_frame:
        # read an image from the capture device or video
        input_image, display_image, output_scale = \
            posenet.utils.process_input(video[frame_count], scale_factor=args.scale_factor, output_stride=output_stride)

        # extract info from image
        heatmaps_result, offsets_result, displacement_fwd_result, displacement_bwd_result = sess.run(
            model_outputs,
            feed_dict={'image:0': input_image}
        )

        # calculate the different key points
        pose_scores, keypoint_scores, keypoint_coords = posenet.decode_multi.decode_multiple_poses(
            heatmaps_result.squeeze(axis=0),
            offsets_result.squeeze(axis=0),
            displacement_fwd_result.squeeze(axis=0),
            displacement_bwd_result.squeeze(axis=0),
            output_stride=output_stride,
            max_pose_detections=10,
            min_pose_score=0.15)
        keypoint_coords *= output_scale

        # show the key points which has been found on the image
        #overlay_image = posenet.draw_skel_and_kp(
        #    display_image, pose_scores, keypoint_scores, keypoint_coords,
        #    min_pose_score=0.15, min_part_score=0.1)

        pose_id = custom.detection.get_pose_id_closest_to_center(
            keypoint_scores, keypoint_coords, display_image.shape[0], display_image.shape[1])
        #cv2.imshow("PLScare", overlay_image)

        # --- Measurement
        symptoms["hand_near_throat"] += 	custom.detection.is_hand_near_throat(pose_id, keypoint_scores, keypoint_coords)
        symptoms["eyes_close"] += 			not custom.detection.are_eyes_open(pose_id, keypoint_scores, keypoint_coords, display_image)
        symptoms["mouth_open"] += 			custom.detection.is_mouth_open(pose_id, keypoint_scores, keypoint_coords, display_image)
        frame_count += 1

        # check the 'q' key to end the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # --- Estimate symptoms
    symptoms["hand_near_throat"] /= frame_count;
    symptoms["eyes_close"] /= frame_count;
    symptoms["mouth_open"] /= frame_count;

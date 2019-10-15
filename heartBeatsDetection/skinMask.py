# Functions used to detect skin on images and extract it as a mask

import numpy as np
import cv2

# define the upper and lower boundaries of the HSV pixel
# intensities to be considered 'skin'
lowerSkin = np.array([0, 48, 80], dtype = "uint8")
upperSkin = np.array([20, 255, 255], dtype = "uint8")

def getSkin(frame, hsvFrame):
    # resize the frame, convert it to the HSV color space,
    # and determine the HSV pixel intensities that fall into
    # the speicifed upper and lower boundaries
    skinMask = cv2.inRange(hsvFrame, lowerSkin, upperSkin)

    # apply a series of erosions and dilations to the mask
    # using an elliptical kernel
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    skinMask = cv2.erode(skinMask, kernel, iterations=2)
    skinMask = cv2.dilate(skinMask, kernel, iterations=2)

    # blur the mask to help remove noise, then apply the
    # mask to the frame
    skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)
    skin = cv2.bitwise_and(frame, frame, mask=skinMask)

    return skin
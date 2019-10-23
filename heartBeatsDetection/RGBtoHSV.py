# Functions used to convert RGB images to HSV

import numpy as np

def RGBimageToHSV(image):

    R = np.array(image[:, :, 0], dtype=np.float).flatten()
    G = np.array(image[:, :, 1], dtype=np.float).flatten()
    B = np.array(image[:, :, 2], dtype=np.float).flatten()

    H = np.empty(len(R))
    H[:] = -1.0
    S = H
    V = H

    R, G, B = R / 255.0, G / 255.0, B / 255.0
    RGB = np.vstack((R, G, B))

    max = np.amax(RGB, axis=0)
    min = np.amin(RGB, axis=0)
    df = max - min

    S = df / max

    mask = (max == 0.0)
    if any(mask):
        S[mask] = 0.0

    mask = (max == min)
    if any(mask):
        H[mask] = 0.0

    mask = (max == R)
    if any(mask):
        H[mask] = ((1/6) * ((G[mask] - B[mask]) / df[mask]) + 1.0) % 1.0

    mask = (max == G)
    if any(mask):
        H[mask] = ((1/6) * ((B[mask] - R[mask]) / df[mask]) + (2/6)) % 1.0

    mask = (max == B)
    if any(mask):
        H[mask] = ((1/6) * ((R[mask] - G[mask]) / df[mask]) + (4/6)) % 1.0

    V = max

    return H, S, V

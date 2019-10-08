import numpy as np


def get_average_value(img):
    return np.average(img[:, :, 0]*0.1140 + img[:, :, 0]*0.5870 + img[:, :, 0]*0.2989)

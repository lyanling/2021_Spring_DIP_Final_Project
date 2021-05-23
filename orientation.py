import numpy as np
import cv2
import math
from scipy import signal

def get_orientaion(img):
    h, w = img.shape
    f_r = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])/4
    f_c = f_r.T
    g_r = signal.convolve2d(img, f_r, mode='same')
    g_c = signal.convolve2d(img, f_c, mode='same')
    theta = np.zeros((h, w), np.float)
    for i in range(h):
        for j in range(w):
            if g_r[i][j] != 0:
                theta[i][j] = math.atan(g_c[i][j]/g_r[i][j])
            elif g_c[i][j] > 0:
                theta[i][j] = math.pi/2
            elif g_c[i][j] < 0:
                theta[i][j] = -math.pi/2
    return theta

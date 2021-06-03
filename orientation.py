import numpy as np
import cv2
import math
from scipy import signal

def get_orientation(img):
    h, w = img.shape

    ex_img = inv(img)/255
    tmp = np.zeros((1, w))
    ex_img = np.append(tmp, ex_img, axis = 0)
    ex_img = np.append(ex_img, tmp, axis = 0)
    tmp = np.zeros((h+2, 1))
    ex_img = np.append(tmp, ex_img, axis = 1)
    ex_img = np.append(ex_img, tmp, axis = 1)

    full = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    times = signal.convolve2d(img, full, mode='same')

    theta_m67 = [np.array([[1, 0, 0], [0, 1, 0], [0, 1, 0]]), np.array([[0, 1, 0], [0, 1, 0], [0, 0, 1]])]
    theta_m45 = [np.array([[1, 0, 0], [0 ,1, 0], [0, 0, 1]]), np.array([[0, 1, 0], [0, 1, 1], [0, 0, 0]]), np.array([[0, 0, 0], [1, 1, 0], [0, 1, 0]])]
    theta_m22 = [np.array([[1, 0, 0], [0, 1, 1], [0, 0, 0]]), np.array([[0, 0, 0], [1, 1, 0], [0, 0, 1]])]
    theta_0 = [np.array([[1, 0, 1], [0 ,1, 0], [0, 0, 0]]), np.array([[0, 0, 0], [1, 1, 1], [0, 0, 0]]), np.array([[0, 0, 0], [0, 1, 0], [1, 0, 1]])]
    theta_22 = [np.array([[0, 0, 1], [1, 1, 0], [0, 0, 0]]), np.array([[0, 0, 0], [0, 1, 1], [1, 0, 0]])]
    theta_45 = [np.array([[0, 1, 0], [1 ,1, 0], [0, 0, 0]]), np.array([[0, 0, 1], [0, 1, 0], [1, 0, 0]]), np.array([[0, 0, 0], [0, 1, 1], [0, 1, 0]])]
    theta_67 = [np.array([[0, 1, 0], [0, 1, 0], [1, 0, 0]]), np.array([[0, 0, 1], [0, 1, 0], [0, 1, 0]])]
    theta_90 = [np.array([[1, 0, 0], [0 ,1, 0], [1, 0, 0]]), np.array([[0, 1, 0], [0, 1, 0], [0, 1, 0]]), np.array([[0, 0, 1], [0, 1, 0], [0, 0, 1]])]

    theta_list = theta_m67 + theta_m45 + theta_m22 + theta_0 + theta_22 + theta_45 + theta_67 + theta_90

    orien = np.full((h, w), -1, np.float)
    orien_img = np.zeros((h, w), np.uint8)
    for i in range(h):
        for j in range(w):
            sum = 0
            cnt = 0
            l = 0
            for k in range(20):
                if np.array_equal(ex_img[i:i+3, j:j+3], theta_list[k]):
                    orien[i][j] = (k+0.5)//2.5*22.5-67.5
                    orien_img[i][j] = int(((k+0.5)//2.5+1)/8*255)
                    break
                if np.logical_and(ex_img[i:i+3, j:j+3], theta_list[k]).sum() == 3:
                    sum += (k+0.5)//2.5*22.5-67.5
                    l += int(((k+0.5)//2.5+1)/8*255)
                    cnt+=1
            if cnt !=0:
                orien[i][j] = sum/cnt
                orien_img[i][j] = l/cnt
    # cv2.imwrite("tmp.jpg", orien_img)  
    return orien

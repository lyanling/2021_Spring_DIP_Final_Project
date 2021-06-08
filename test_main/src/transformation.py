# from types import new_class
import numpy as np
import math
import random
from modules import geo_modify as gm
from numpy.linalg import inv
import cv2 as cv
# import pickle

def adjust_connect_list(connect_list, label, shift_value):
    connect_labels = list(connect_list[label-1])
    for connect_label in connect_labels:
        r = connect_list[connect_label-1][label][0] + shift_value[0]
        c = connect_list[connect_label-1][label][1] + shift_value[1]
        connect_list[connect_label-1][label] = (r, c)

def shift_part(parts, label, shift_value):
    point_num = len(parts[label-1])
    for i in range(point_num):
        point = parts[label-1][i]
        # print(parts[label-1])
        # print(point, shift_value)
        r = point[0] + shift_value[0]
        c = point[1] + shift_value[1]
        parts[label-1][i] = (r, c)


def adjust_connect_list_2(h, w, connect_list, label, M):
    # get the new position of connecting point, and adjust the connect_list
    # connect_list: [{part1's connection}, {part2's connection}, {part3's connection}]
        # part1's cpnnection: {2: point A, 3: point B}  -> connect to part2's point A, and part3's point B
    connect_labels = list(connect_list[label-1])
    for connect_label in connect_labels:
        point = connect_list[connect_label-1][label]
        (x, y) = gm.to_cart(point[1], point[0], h)
        in_vec = np.array([x, y, 1])
        u, v, z = np.dot(M, in_vec)
        new_point = gm.to_img_coord(u, v, h)
        c_i = max(min(h-1, round(new_point[0])), 0)
        c_j = max(min(w-1, round(new_point[1])), 0)
        connect_list[connect_label-1][label] = (c_i, c_j)

def getPartImg(h, w, part, extend):
    part_img = np.zeros([h, w])
    part_img.fill(255)
    part_pos = np.array(part).T + extend
    part_img[tuple([part_pos[0], part_pos[1]])] = 0
    # for point in part:
    #     part_img[(point[0] + extend, point[1] + extend)] = 0
    return part_img

def getPartFromImg(part_img):
    part = []
    h, w  = part_img.shape
    for i in range(h):
        for j in range(w):
            point = (i, j)
            if (part_img[point] == 0):
                part.append(point)
    return part

def label_to_parts(label):
    parts = []
    for part_id in range(label.max(), 0, -1):
        part = [tuple(coords) for coords in np.argwhere(label == part_id)]
        parts.append(part)
    return parts

def transform(img, parts, connect_list, aver_orientation):
    # parts = label_to_parts(label)
    
    h, w = img.shape
    extend = 100
    h += extend*2
    w += extend*2

    new_img = np.zeros([h, w])
    new_img.fill(255)
    new_img[extend:h-extend, extend:w-extend] = img

    for i in range(len(parts)):
        # shift_part(parts, i+1, (extend, extend))
        adjust_connect_list(connect_list, i+1, (extend, extend))

    trans_parts = []
    theta_range = [-10, 10]
    scale_range = [0.9, 1.1]

    for n in range(len(parts)):
        part = parts[n]
        part_img = getPartImg(h, w, part, extend)   # convert the part into an image
        part_idx = np.where(part_img==0)
        max_x, min_x, max_y, min_y = part_idx[0].max(), part_idx[0].min(), part_idx[1].max(), part_idx[1].min()
        center_x = (max_x+min_x)//2
        center_y = (max_y+min_y)//2

        center = (center_x, center_y)  # center at the point with smallest r
        cart_center = gm.to_cart(center[1], center[0], h)   # to cartesian coordinate

        # translation
        T = np.array([[1, 0, -cart_center[0]], [0, 1, -cart_center[1]], [0, 0, 1]])
        TB = np.array([[1, 0, cart_center[0]], [0, 1, cart_center[1]], [0, 0, 1]])  # translate back

        # scaling
        scale_mag = random.uniform(scale_range[0], scale_range[1])
        S = np.array([[scale_mag, 0, 0], [0, scale_mag, 0], [0, 0, 1]])

        # rotation
        dt = random.uniform(theta_range[0], theta_range[1]) / 360 * (math.pi)
        R = np.array([[math.cos(dt), -math.sin(dt), 0], [math.sin(dt), math.cos(dt), 0], [0, 0, 1]])
        aver_orientation[n] += dt

        # transform matrix
        M = np.matmul(S, T)
        M = np.matmul(R, M)
        M = np.matmul(TB, M)
        M_inv = inv(M)

        # backward transformation

        trans_img = np.zeros_like(part_img)
        trans_img.fill(255)
        trans_pos = np.meshgrid(range(h), range(w), indexing='ij')
        trans_pos[0] = trans_pos[0].reshape((1, -1))
        trans_pos[1] = trans_pos[1].reshape((1, -1))
        cart_x = trans_pos[1]
        cart_y = h-1-trans_pos[0]
        trans_cart = np.r_[cart_x, cart_y, np.ones((1, trans_pos[0].size))]
        trans_cart = np.matmul(M_inv, trans_cart)
        trans_pos[0] = h-1-trans_cart[1]
        trans_pos[1] = trans_cart[0]
        trans_check_1 = np.array(trans_pos[0]).reshape((h, w))
        trans_check_2 = np.array(trans_pos[1]).reshape((h, w))
        trans_pos[0][trans_pos[0] < 0] = 0
        trans_pos[1][trans_pos[1] < 0] = 0
        trans_pos[0][trans_pos[0] > h-1] = h-1
        trans_pos[1][trans_pos[1] > w-1] = w-1

        trans_pos[0] = np.round(trans_pos[0]).astype(int)
        trans_pos[1] = np.round(trans_pos[1]).astype(int)

        trans_img[:, :] = part_img[trans_pos].reshape((h, w))
        trans_img = np.where(trans_check_1 < 0, 255, trans_img)
        trans_img = np.where(trans_check_1 > h-1, 255, trans_img)
        trans_img = np.where(trans_check_2 < 0, 255, trans_img)
        trans_img = np.where(trans_check_2 > w-1, 255, trans_img)
        # cv.imshow(':(', trans_img)
        # cv.waitKey(0)
        # cv.waitKey(1)
        # cv.destroyAllWindows()
        # cv.waitKey(1)
        # interp may be slow :( (

        # for i in range(h):
        #     for j in range(w):
        #         (x, y) = gm.to_cart(j, i, h)    # to cartesian coordinate
        #         in_vec = np.array([x, y, 1])    # input vector
        #         u, v, z = np.dot(M_inv, in_vec)
        #         c_point = gm.to_img_coord(u, v, h)  # to img coordinate
        #         # trans_img[i, j] = gm.bilinear_interpolation(part_img, c_point)    # bilinear interpolation is not applicable in this case
        #         c_i = max(min(h-1, round(c_point[0])), 0)   # find the nearest integer
        #         c_j = max(min(w-1, round(c_point[1])), 0)
        #         trans_img[i, j] = part_img[c_i, c_j]

        # adjust connect point pair
        adjust_connect_list_2(h, w, connect_list, n+1, M)

        # get new part
        # new_part = getPartFromImg(trans_img)
        new_part = np.array(np.where(trans_img == 0)).T
        trans_parts.append(new_part)
    
    return new_img, trans_parts, connect_list, aver_orientation

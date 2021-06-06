# from types import new_class
import numpy as np
import math
import random
from . import geo_modify as gm
from numpy.linalg import inv

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
        r = point[0] + shift_value[0]
        c = point[1] + shift_value[1]
        parts[label-1][i] = (r, c)


def adjust_connect_list_2(h, w, connect_list, label, M):
    # print(label)
    # print(len(connect_list))
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
    for point in part:
        part_img[(point[0], point[1])] = 0
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

def transform(img, parts, connect_list):
    h, w = img.shape
    extend = 10
    h += extend*2
    w += extend*2

    new_img = np.zeros([h, w])
    new_img.fill(255)
    new_img[extend:h-extend, extend:w-extend] = img

    for i in range(len(parts)):
        shift_part(parts, i+1, (extend, extend))
        adjust_connect_list(connect_list, i+1, (extend, extend))

    trans_parts = []
    theta_range = [-10, 10]
    scale_range = [0.9, 1.1]

    for n in range(len(parts)):
        part = parts[n]
        part_img = getPartImg(h, w, part, extend)
        center = min(part)
        print(center)
        cart_center = gm.to_cart(center[1], center[0], h)
        print(cart_center)
        # translation
        T = np.array([[1, 0, -cart_center[0]], [0, 1, -cart_center[1]], [0, 0, 1]])
        TB = np.array([[1, 0, cart_center[0]], [0, 1, cart_center[1]], [0, 0, 1]])

        # scaling
        scale_mag = random.uniform(scale_range[0], scale_range[1])
        S = np.array([[scale_mag, 0, 0], [0, scale_mag, 0], [0, 0, 1]])

        # rotation
        dt = random.uniform(theta_range[0], theta_range[1]) / 360 * (math.pi)
        R = np.array([[math.cos(dt), -math.sin(dt), 0], [math.sin(dt), math.cos(dt), 0], [0, 0, 1]])

        # transform matrix
        # M = T
        M = np.matmul(S, T)
        M = np.matmul(R, M)
        M = np.matmul(TB, M)
        M_inv = inv(M)

        # backward transformation
        trans_img = np.zeros_like(part_img)
        trans_img.fill(255)
        for i in range(h):
            for j in range(w):
                (x, y) = gm.to_cart(j, i, h)
                in_vec = np.array([x, y, 1])
                u, v, z = np.dot(M_inv, in_vec)
                c_point = gm.to_img_coord(u, v, h)
                # trans_img[i, j] = gm.bilinear_interpolation(part_img, c_point)
                c_i = max(min(h-1, round(c_point[0])), 0)
                c_j = max(min(w-1, round(c_point[1])), 0)
                # print(c_i, c_j)
                trans_img[i, j] = part_img[c_i, c_j]


        # # change connect point pair
        adjust_connect_list_2(h, w, connect_list, n+1, M)

        # get new part
        new_part = getPartFromImg(trans_img)
        # new_part = getPartFromImg(part_img)
        trans_parts.append(new_part)
    
    return new_img, trans_parts, connect_list
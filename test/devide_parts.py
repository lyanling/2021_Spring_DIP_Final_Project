import numpy as np
import cv2 as cv

def find_next_pixel(img_bool, orientation, i, j, i_s, j_s, threshold_angle = 30):
    # the center pixel
    i_c = i-i_s
    j_c = j-j_s
    # print(i_c, j_c)
    # print(orientation.shape)
    # print(img_bool.shape)
    o_c = orientation[i_c][j_c]
    m, n = img_bool.shape
    
    candidates = []
    for x in range(m):
        for y in range(n):
            # check if there is another pixel has similar orientation
            if x == i_c and y == j_c:
                continue
            if (not img_bool[x, y]):
                continue
            o = orientation[x][y]
            if get_orient_diff(o, o_c) <= threshold_angle:
                candidates.append((x+i_s, y+j_s))
            # if o_c >= 90 - threshold_angle and o <= -90 + threshold_angle:
            #     if (90 - o_c) + (o + 90) <= threshold_angle:
            #         candidates.append((x+i_s, y+j_s))
            # if o >= 90 - threshold_angle and o_c <= -90 + threshold_angle:
            #     if (90 - o) + (o_c + 90) <= threshold_angle:
            #         candidates.append((x+i_s, y+j_s))
    return candidates

def find_next_pixel_2(img_bool, i_c, j_c, i_s, j_s, i_d, j_d):
    # print(img.shape)
    points = []
    for i in range(i_s, i_d+1):
        for j in range(j_s, j_d+1):
            if i == i_c and j == j_c:
                continue
            if not img_bool[i, j]:
                continue
            points.append((i, j))
    # print(points)
    return points

def get_orient_diff(orient_1, orient_2):
    max_orient = max(orient_1, orient_2)
    min_orient = min(orient_1, orient_2)
    diff = max_orient - min_orient
    diff_2 = (180 - max_orient) + min_orient
    diff = min(diff, diff_2)

    return diff

def devide_parts(img, orientation, critical_points):
    m, n = img.shape
    # adjust orientation
    for i in range(m):
        for j in range(n):
            if (img[i, j] == 0) and (orientation[i, j] < 0):
                orientation[i, j] += 90
    orientation[img == 255] = -1

    img_bool = np.where(img == 255, False, True)    # True means the unlabeled part
    img_label = np.zeros_like(img)  # labeling the different part with number (start from 1, 0 for white parts)
    searching_size = 2
    part_count = 0
    parts = []
    for x in range(m):
        for y in range(n):
            if not img_bool[x][y]:
                continue
            # found a new pixel hasn't been devided
            part = set()
            # part.add((x, y))
            candidates = [(x, y)]
            while(len(candidates) > 0):
                x_cur, y_cur = candidates[-1]
                candidates.pop()
                if (x_cur, y_cur) in part:
                    continue
                part.add((x_cur, y_cur))
                img_bool[x_cur][y_cur] = False
                img_label[x_cur][y_cur] = part_count + 1
                x_s, x_d = (max(0, x_cur - 2), min(m-1, x_cur+2))
                y_s, y_d = (max(0, y_cur-2), min(n-1, y_cur+2))
                next_pixel_pos = find_next_pixel(img_bool[x_s:x_d+1, y_s:y_d+1], orientation[x_s:x_d+1, y_s:y_d+1], x_cur, y_cur, x_s, y_s)
                candidates += next_pixel_pos
            parts.append(part)
            part_count += 1


    # c_point_set = set(critical_points)
    # for point in critical_points:
    #     # handling points
    #     x, y = point
    #     # if not img_bool[x][y]:
    #     #     continue
    #     candidates = [(x, y)]
    #     part = set()
    #     while(len(candidates) > 0):
    #         x_cur, y_cur = candidates[-1]
    #         candidates.pop()
    #         if (x_cur, y_cur) in part:
    #             continue
    #         if (x_cur, y_cur) in c_point_set and (x_cur, y_cur) != (x, y):
    #             continue
    #         part.add((x_cur, y_cur))
    #         if not (x_cur, y_cur) in c_point_set:
    #             img_bool[x_cur][y_cur] = False
    #         # img_label[x_cur][y_cur] = part_count + 1
    #         x_s, x_d = max(0, x_cur - 1), min(m-1, x_cur+1)
    #         y_s, y_d = max(0, y_cur - 1), min(n-1, y_cur+1)
    #         # print(x_cur, x_s, x_d, y_cur, y_s, y_d)
    #         next_pixel_pos = find_next_pixel_2(img_bool, x_cur, y_cur, x_s, y_s, x_d, y_d)
    #         candidates += next_pixel_pos
    #     parts.append(part)
    #     part_count += 1
    return parts

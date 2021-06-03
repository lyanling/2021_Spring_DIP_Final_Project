import numpy as np
import cv2 as cv
from orientation_comparison import has_similar_orientation
def find_next_pixel(img_bool, orientation, i, j, i_s, j_s):
    # the center pixel
    i_c = i-i_s
    j_c = j-j_s
    o_c = orientation[i_c][j_c]
    m, n = img_bool.shape
    threshold_angle = 45
    candidates = []
    for x in range(m):
        for y in range(n):
            # check if there is another pixel has similar orientation
            if x == i_c and y == j_c:
                continue
            if not img_bool[x][y]:
                continue
            o = orientation[x][y]
            if has_similar_orientation(o_c, o, threshold=threshold_angle)
            # if abs(o-o_c) <= threshold_angle:
            #     candidates.append((x+i_s, y+j_s))
            # if o_c >= 90 - threshold_angle and o <= -90 + threshold_angle:
            #     if (90 - o_c) + (o + 90) <= threshold_angle:
            #         candidates.append((x+i_s, y+j_s))
            # if o >= 90 - threshold_angle and o_c <= -90 + threshold_angle:
            #     if (90 - o) + (o_c + 90) <= threshold_angle:
            #         candidates.append((x+i_s, y+j_s))
    return candidates


def devide_parts(img, orientation):
    # , critical_points
    img_bool = np.where(img == 255, False, True)    # True means the unlabeled part
    img_check = np.where(img == 255, False, True)
    img_label = np.zeros_like(img)  # labeling the different part with number (start from 1, 0 for white parts)
    m, n = img.shape
    searching_size = 2
    part_count = 0
    parts = []
    for x in range(m):
        for y in range(n):
            # x, y = point
            if not img_bool[x][y]:
                continue
            # found a new pixel hasn't been devided
            part = set()
            part.add((x, y))
            candidates = [(x, y)]
            while(len(candidates) > 0):
                x_cur, y_cur = candidates[-1]
                candidates.pop()
                if (x_cur, y_cur) in part:
                    continue
                part.add((x_cur, y_cur))
                img_bool[x_cur][y_cur] = False
                img_label[x_cur][y_cur] = part_count + 1
                x_s, x_d = max(0, x_cur - 2), min(m-1, x_cur+2)
                y_s, y_d = max(0, y_cur-2), min(n-1, y_cur+2)
                next_pixel_pos = find_next_pixel(img_check[x_s:x_d+1][y_s:y_d+1], orientation[x_s:x_d+1][y_s:y_d+1], x_cur, y_cur, x_s, y_s)
                candidates += next_pixel_pos
            parts.append(part)
            part_count += 1
    return parts
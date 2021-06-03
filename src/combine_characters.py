import cv2 as cv
import numpy as np
from orientation_comparison import has_similar_orientation

def find_combine_point(img, ori, side, count):
    pos_x, pos_y = np.where(img == 0)
    sorted_idx = np.argsort(pos_x)
    if side=='left':    # find the right-most point for left img
        cpoint_pos = tuple(pos_x[sorted_idx[-count:]], pos_y[sorted_idx[-count:]])
        cpoint_ori = tuple(pos_x[sorted_idx[-count:]], pos_y[sorted_idx[-count:]])
    elif side=='right':   # find the left-most point for right img 
        cpoint_pos = tuple(pos_x[sorted_idx[:count]], pos_y[sorted_idx[:count]])
        cpoint_ori = tuple(pos_x[sorted_idx[:count]], pos_y[sorted_idx[:count]])
    else:
        print('find_combine_point: argument "side" should be either "left" or "right"')
        return None, None
    return cpoint_pos, cpoint_ori


def match_points(pos_right, pos_left, ori_left, ori_right, floor_left, floor_right):
    # straight line
    if not has_similar_orientation(ori_left, ori_right, threshold=20):
        return False
    height_left = pos_left[0] - floor_left
    heighr_right = pos_right[0] - floor_right
    if ori_left > 0 and height_left >= height_right:
        return True
    if ori_left < 0 and height_left <= height_right:
        return True
    return False

def find_best_match(matches):
    for match in matches:
        pos_right, pos_left, ori_left, ori_right, floor_left, floor_right = match

    return

def draw_line(pos_left, pos_right, ori_left, ori_right, floor_left, floor_right):

    return

def combine_parts(img_left, img_right, ori_left, ori_right, floor_left, floor_right, count=5):
    cpoint_pos_left, cpoint_ori_left = find_combine-point(img_left, ori_left, 'left', count)
    cpoint_pos_right, cpoint_ori_right = find_combine-point(img_right, ori_right, 'right', count)
    matches = []
    for i in range(count):
        pos_left = cpoint_pos_left[i]
        ori_left = cpoint_ori_left[i]
        for j in range(count):
            pos_right = cpoint_pos_right[j]
            ori_right = cpoint_ori_right[j]
            if match_points(pos_right, pos_left, ori_left, ori_right, floor_left, floor_right):
                matches.append((pos_right, pos_left, ori_left, ori_right, floor_left, floor_right))
            best_match = find_best_match(matches)
            draw_line()


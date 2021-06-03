import cv2 as cv
import numpy as np

def find_combine_point(img, ori, side, count):
    I = np.where(img == 0)
    if side=='left':    # find the right-most point for left img
        
        pass
    if side=='right':   # find the left-most point for right img 
        pass
    return cpoint_pos, cpoint_ori

def match_points(pos_right, pos_left, ori_left, ori_right, floor_left, floor_right):
    # straight line
    if 
    return

def draw_line():

    return

def combine_parts(img_left, img_right, ori_left, ori_right, floor_left, floor_right, count=5):
    cpoint_pos_left, cpoint_ori_left = find_combine-point(img_left, ori_left, 'left', count)
    cpoint_pos_right, cpoint_ori_right = find_combine-point(img_right, ori_right, 'right', count)
    for i in range(count):
        pos_left = cpoint_pos_left[i]
        ori_left = cpoint_ori_left[i]
        for j in range(count):
            pos_right = cpoint_pos_right[j]
            ori_right = cpoint_ori_right[j]
            if match_points(pos_right, pos_left, ori_left, ori_right, floor_left, floor_right):
                draw_line()


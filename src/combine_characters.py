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


def match_points(pos_left, pos_right, ori_left, ori_right, floor_left, floor_right):
    # straight line
    if not has_similar_orientation(ori_left, ori_right, threshold=20):
        return False
    height_left = pos_left[0] - floor_left
    height_right = pos_right[0] - floor_right
    if ori_left > 0 and height_left >= height_right:
        return True
    if ori_left < 0 and height_left <= height_right:
        return True
    return False

def find_best_match(matches, expected_dist):
    dist = []
    for match in matches:
        pos_left, pos_right, ori_left, ori_right, floor_left, floor_right = match
        height_left = pos_left[0] - floor_left
        height_right = pos_right[0] - floor_right
        if height_left == height_right:
            dist.append(0)
            continue
        angle_left = ori_left * (np.pi / 180)
        angle_right = ori_right * (np.pi / 180)
        angle_line = (angle_left + angle_right) / 2
        dist.append(abs(height_left-height_right) / np.tan(angle_line))
    dist = np.array(dist)
    diff = np.abs(dist - expected_dist)
    sorted_idx = np.argsort(diff)
    best_match = matches[sorted_idx[0]]
    return best_match, dist[sorted_idx[0]]

def draw_line(img_left, img_right, match, space):
    pos_left, pos_right, ori_left, ori_right, floor_left, floor_right = match
    m_l, n_l = img_left.shape
    m_r, n_r = img_right.shape
    img_combined = np.zeros((max(m_l, m_r), n_l + n_r + space))
    if space == 0:
        img_combined[, :n_l] = img_left
    
    return

def combine_parts(img_left, img_right, ori_left, ori_right, floor_left, floor_right, expected_dist, count=5):
    cpoint_pos_left, cpoint_ori_left = find_combine_point(img_left, ori_left, 'left', count)
    cpoint_pos_right, cpoint_ori_right = find_combine_point(img_right, ori_right, 'right', count)
    matches = []
    for i in range(count):
        pos_left = cpoint_pos_left[i]
        ori_left = cpoint_ori_left[i]
        for j in range(count):
            pos_right = cpoint_pos_right[j]
            ori_right = cpoint_ori_right[j]
            if match_points(pos_left, pos_right, ori_left, ori_right, floor_left, floor_right):
                matches.append((pos_left, pos_right, ori_left, ori_right, floor_left, floor_right))
            best_match, dist = find_best_match(matches, expected_dist)
            img_combined, floor_combined = draw_line(img_left, img_right, best_match, dist)
    return img_combined, floor_combined


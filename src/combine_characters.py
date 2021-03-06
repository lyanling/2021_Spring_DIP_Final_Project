import numpy as np
from orientaion_comparison import has_similar_orientation_2
import random

def find_combine_point(img, ori, side, count):
    pos_x, pos_y = np.where(img == 0)
    sorted_idx = np.argsort(pos_x)
    if side=='left':    # find the right-most point for left img
        cpoint_pos = tuple([pos_x[sorted_idx[-count:]], pos_y[sorted_idx[-count:]]])
        cpoint_ori = ori[cpoint_pos]
    elif side=='right':   # find the left-most point for right img 
        cpoint_pos = tuple([pos_x[sorted_idx[:count]], pos_y[sorted_idx[:count]]])
        cpoint_ori = ori[cpoint_pos]
    else:
        print('find_combine_point: argument "side" should be either "left" or "right"')
        return None, None
    cpoint_pos = np.array(cpoint_pos).T
    cpoint_ori = np.array(cpoint_ori).T
    return cpoint_pos, cpoint_ori


def match_points(pos_left, pos_right, ori_left, ori_right, floor_left, floor_right):
    # straight line
    if not has_similar_orientation_2(ori_left, ori_right, threshold=20):
        return False
    height_left = floor_left - pos_left[0]
    height_right = floor_right - pos_right[0]
    if ori_left > 0 and height_left >= height_right:
        return True
    if ori_left < 0 and height_left <= height_right:
        return True
    return False

def find_best_match(matches, expected_dist, floor_left, floor_right):
    if len(matches) == 0:
        return None
    dist = []
    for match in matches:
        pos_left, pos_right, ori_left, ori_right = match
        height_left = floor_left - pos_left[0]
        height_right = floor_right - pos_right[0]
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
    return best_match

def kerning(img_left, img_right, floor_left, floor_right, space, last_width):
    img_left = img_left[:, -last_width:]
    left_pos_x, left_pos_y = np.where(img_left == 0)
    height_left = floor_left - left_pos_x
    right_pos_x, right_pos_y = np.where(img_right == 0)
    height_right = floor_right - right_pos_x
    min_h, max_h = min(height_left.min(), height_right.min()), max(height_right.max(), height_left.max())
    dist = []
    for h in range(min_h, max_h + 1):
        pos_left = left_pos_y[height_left == h]
        pos_right = right_pos_y[height_right == h]
        if pos_left.size == 0 or pos_right.size == 0:
            dist.append(np.inf)
            continue
        pos_left = img_left.shape[1] - pos_left.max()
        pos_right = pos_right.min()
        dist.append(pos_left + pos_right - 1)
    dist = np.array(dist)
    min_dist = dist.min()
    if min_dist == np.inf:
        return space
    else:
        return (space - min_dist)

def getSlope(ori):  # dr, dc
    if (ori > 90):
        ori -= 180
    if (ori <= -56 and ori > 78):    # -67
        return 0, (3, 2)
    elif (ori <= -34):  # -45
        return 1, (3, 3)
    elif (ori <= -11):  # -22
        return 2, (2, 3)
    elif (ori <= 11):   # 0
        return 3, (1, 3)
    elif (ori <= 33):   # 22
        return 4, (2, 3)
    elif (ori <= 56):   # 45
        return 5, (3, 3)
    elif (ori <= 78):   # 67
        return 6, (3, 2)
    return 7, (3, 1)       # 90 / -90

def get_patterns():
    theta_m67 = [np.array([[1, 0], [0, 1], [0, 1]]), np.array([[1, 0], [1, 0], [0, 1]])]
    theta_m45 = [np.array([[1, 0, 0], [0 ,1, 0], [0, 0, 1]])]
    theta_m22 = [np.array([[1, 0, 0], [0, 1, 1]]), np.array([[1, 1, 0], [0, 0, 1]])]
    theta_0 = [np.array([[1, 1, 1]])]
    theta_22 = [np.array([[0, 0, 1], [1, 1, 0]]), np.array([[0, 1, 1], [1, 0, 0]])]
    theta_45 = [np.array([[0, 0, 1], [0, 1, 0], [1, 0, 0]])]
    theta_67 = [np.array([[0, 1], [0, 1], [1, 0]]), np.array([[0, 1], [1, 0], [1, 0]])]
    theta_90 = [np.array([[0, 1, 0], [0, 1, 0], [0, 1, 0]])]
    pattern_list = []
    pattern_list.append(theta_m67)
    pattern_list.append(theta_m45)
    pattern_list.append(theta_m22)
    pattern_list.append(theta_0)
    pattern_list.append(theta_22)
    pattern_list.append(theta_45)
    pattern_list.append(theta_67)
    pattern_list.append(theta_90)
    for pattern in pattern_list:
        for i in range(len(pattern)):
            pattern[i] = (pattern[i] ^ 1) * 255
    return pattern_list

def chooseAPattern(patterns):
    p = random.uniform(0, len(patterns))
    return patterns[p]

def draw_line(img_left, img_right, match, space, pattern_list, floor_left, floor_right, last_width):
    to_draw = False
    dc = -1
    if match is not None:
        pos_left, pos_right, ori_left, ori_right = match
        pattern_idx, slope = getSlope(ori_left)
        d_pos = pos_right - pos_left
        dc = ((d_pos[0] + slope[0] - 1) // slope[0]) * slope[1]
        to_draw = True
        new_space = dc - pos_right[1]

    m_l, n_l = img_left.shape
    m_r, n_r = img_right.shape
    floor_above = max(floor_left, floor_right, 0)
    floor_below = max(m_l-floor_left , m_r - floor_right , 0)     # -1
    if (dc <= 0):
        new_space = kerning(img_left, img_right, floor_left, floor_right, space, last_width)
        to_draw = False

    # combine two imgs
    img_combined = np.zeros((floor_above + floor_below, max(n_l + n_r + round(new_space), n_l) ))
    img_combined.fill(255)
    start_left = floor_above - floor_left   # the highest point's position of left_img
    start_right = floor_above - floor_right     # the highest point's position of right_img
    img_combined[start_left:start_left+m_l, :n_l] = img_left
    img_right_paste_area = img_combined[start_right:start_right+m_r, -n_r:]
    img_right_paste_area = np.where(img_right == 0, 0, img_right_paste_area)
    img_combined[start_right:start_right+m_r, -n_r:] = img_right_paste_area
    
    if (not to_draw):
        return img_combined, floor_above, start_right
    # draw
    # get line pattern
    patterns = pattern_list[pattern_idx]
    pattern_r = 0
    if ori_left > 0:
        pattern_r = -(slope[0]-1)   # if orientation > 0, start from the most left, lowest pixel of the pattern
    current_c = pos_left[1] + 1
    current_r = pos_left[0] + start_left

    while (current_c < (pos_left[1] + dc)):
        pattern = chooseAPattern(patterns)
        rr = current_r + pattern_r
        img_combined[rr:rr + slope[0], current_c:current_c + slope[1]] &= pattern
        if (rr - 1 >= 0):
            img_combined[rr-1:rr-1 + slope[0], current_c:current_c + slope[1]] &= pattern   # bolding
        if (rr + 1 < img_combined.shape[0]):
            img_combined[rr+1:rr+1 + slope[0], current_c:current_c + slope[1]] &= pattern   # bolding
        current_r += slope[0]
        current_c += slope[1]
        
    return img_combined, floor_above, start_right

def combine_char(img_left, img_right, ori_left, ori_right, floor_left, floor_right, expected_dist, last_width, count=5):
    if img_left is None:
        return img_right, floor_right, ori_right, img_right.shape[1] // 2
    cpoint_pos_left, cpoint_ori_left = find_combine_point(img_left, ori_left, 'left', count)
    cpoint_pos_right, cpoint_ori_right = find_combine_point(img_right, ori_right, 'right', count)
    matches = []
    pattern_list = get_patterns()
    for i in range(count):
        pos_left = cpoint_pos_left[i]
        orient_left = cpoint_ori_left[i]
        for j in range(count):
            pos_right = cpoint_pos_right[j]
            orient_right = cpoint_ori_right[j]
            if match_points(pos_left, pos_right, orient_left, orient_right, floor_left, floor_right):
                matches.append((pos_left, pos_right, orient_left, orient_right))
    best_match = find_best_match(matches, expected_dist, floor_left, floor_right)
    img_combined, floor_combined, start_right = draw_line(img_left, img_right, best_match, expected_dist, pattern_list, floor_left, floor_right, last_width)
    next_orient = np.zeros(img_combined.shape)
    next_orient[start_right:start_right+ori_right.shape[0], -ori_right.shape[1]:] = ori_right
    return img_combined, floor_combined, next_orient, img_right.shape[1] //2
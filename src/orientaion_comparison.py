import numpy as np

def get_orient_diff(orient_1, orient_2):
	max_orient = min(max(orient_1, orient_2), 180)
	min_orient = max(min(orient_1, orient_2), 0)
	diff = max_orient - min_orient
	diff_2 = (180 - max_orient) + min_orient
	diff = min(diff, diff_2)
	return diff

def has_similar_orientation(ori_1, ori_2, threshold_angle=20):
    if abs(ori_1 - ori_2) <= threshold_angle:
        return True
    elif ori_1 >= 90 - threshold_angle and ori_2 <= -90 + threshold_angle:
        if (90 - ori_1) + (ori_2 + 90) <= threshold_angle:
            return True
    elif ori_2 >= 90 - threshold_angle and ori_2 <= -90 + threshold_angle:
        if (90 - ori_2) + (ori_1 + 90) <= threshold_angle:
            return True
    return False

def has_similar_orientation_2(ori_1, ori_2, threshold_angle=20):
    if (get_orient_diff(ori_1, ori_2) <= threshold_angle):
    	return True
    else:
    	return False
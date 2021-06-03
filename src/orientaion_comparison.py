import numpy as np

def has_similar_orientation(ori_1, ori_2, threshold=20):
    if abs(ori_1 - ori_2) <= threshold_angle:
        return True
    elif ori_1 >= 90 - threshold_angle and ori_2 <= -90 + threshold_angle:
        if (90 - ori_1) + (ori_2 + 90) <= threshold_angle:
            return True
    elif ori_2 >= 90 - threshold_angle and ori_2 <= -90 + threshold_angle:
        if (90 - ori_2) + (ori_1 + 90) <= threshold_angle:
            return True
    return False

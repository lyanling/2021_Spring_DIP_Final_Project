import numpy as np
from . import geo_modify as gm


def adjust_orientation(img, orientation):
    h, w = img.shape
    for i in range(h):
        for j in range(w):
            if (img[i, j] == 0) and (orientation[i, j] < 0):
                orientation[i, j] += 180
    orientation[img == 255] = -1

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

def combine_parts(img, bold_parts, connect_list, aver_orientation):
	# parts: 
	# connect_points: [[part1's connect_points_pairs], [], [], ...]
	# part1's connect_points_pairs = [(X, part1's pointA, partX's point C), 
								# (Y, part1's point B, partY's point D), ...]

	out_img = np.zeros_like(img)
	out_img.fill(255)

	# orientation = get_orientation(img)
	# adjust_orientation(img, orientation)
	parts_num = len(bold_parts)

	for i in range(len(connect_list)-1, -1, -1):
		connect_labels = list(connect_list[i])
		c_label = i+1
		if len(connect_labels) > 0:		# connect this part to bigger part
			label = connect_labels[0]
			if (c_label <= label):		# the smaller label, the bigger part
				continue
			c_connect_point = connect_list[label-1][c_label]	# the point in this part that connects another part
			label_connect_point = connect_list[c_label-1][label]	# the point in another part that connects this part
			shift_value = (label_connect_point[0] - c_connect_point[0], label_connect_point[1] - c_connect_point[1])
			shift_part(bold_parts, c_label, shift_value)
			adjust_connect_list(connect_list, c_label, shift_value)	# adjust the information of connecting points, 
																		# since the position has changed

	min_h, min_w = 1000, 1000
	max_h, max_w = -1000, -1000

	for part in bold_parts:
		r, c = np.array(part).T
		min_h = min(min_h, min(r))
		min_w = min(min_w, min(c))
		max_h = max(min_h, max(r))
		max_w = max(min_w, max(c))
	h = max_h - min_h
	w = max_w - min_w

	# method 1
	ori_img = np.zeros([h, w])
	ori_img.fill(-1)
	n = 0
	for part in bold_parts:
		r, c = np.array(part).T
		r -= min_h
		c -= min_w
		out_img[r, c] = 0
		ori = aver_orientation[n]
		ori_img[r, c] = ori
	
	return out_img, ori_img


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

def combine_parts(img, parts, connect_list):
	# parts: 
	# connect_points: [[part1's connect_points_pairs], [], [], ...]
	# part1's connect_points_pairs = [(X, part1's pointA, partX's point C), 
								# (Y, part1's point B, partY's point D), ...]

	out_img = np.zeros_like(img)
	out_img.fill(255)

	# orientation = get_orientation(img)
	# adjust_orientation(img, orientation)
	parts_num = len(parts)

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
			shift_part(parts, c_label, shift_value)
			adjust_connect_list(connect_list, c_label, shift_value)	# adjust the information of connecting points, 
																		# since the position has changed

	for part in parts:
		for point in part:
			out_img[point] = 0
	
	return out_img


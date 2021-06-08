import numpy as np
from . import geo_modify as gm


def adjust_connect_list(connect_list, c_label, new_label, shift_value):
	connect_labels = list(connect_list[c_label-1])
	for connect_label in connect_labels:
		if connect_label == new_label:
			continue
		r = connect_list[connect_label-1][c_label][0] + shift_value[0]
		c = connect_list[connect_label-1][c_label][1] + shift_value[1]
		connect_list[connect_label-1].pop(c_label, None)
		connect_list[connect_label-1][new_label] = (r, c)
		connect_list[new_label-1][connect_label] = connect_list[c_label-1][connect_label]

def shift_part(parts, label, shift_value):
    point_num = len(parts[label-1])
    for i in range(point_num):
        point = parts[label-1][i]
        r = point[0] + shift_value[0]
        c = point[1] + shift_value[1]
        parts[label-1][i] = (r, c)

def merge_parts(parts, c_label, new_label):
	parts[new_label-1] += parts[c_label-1]
	parts[c_label-1].clear()

def adjust_connect_parts(bold_parts, connect_list, new_connect_labels, shift_value):
	for label in new_connect_labels:
		shift_part(bold_parts, label, shift_value)
		adjust_connect_list(connect_list, label, shift_value)

def combine_parts(img, bold_parts, connect_list, aver_orientation):
	# parts: 
	# connect_points: [[part1's connect_points_pairs], [], [], ...]
	# part1's connect_points_pairs = [(X, part1's pointA, partX's point C), 
								# (Y, part1's point B, partY's point D), ...]


	# orientation = get_orientation(img)
	# adjust_orientation(img, orientation)
	parts_num = len(bold_parts)
	new_connect_list = []
	for i in range(len(connect_list)):
		new_connect_list.append([])

	for i in range(len(connect_list)-1, -1, -1):
		connect_labels = list(connect_list[i])
		c_label = i+1
		for i in range(len(connect_labels)):		# connect this part to bigger part
			label = connect_labels[i]
			# if (c_label <= label and (len(new_connect_list[c_label-1]) > 0)):		# the smaller label, the bigger part
			# 	continue
			if not c_label in connect_list[label-1].keys():
				continue
			c_connect_point = connect_list[label-1][c_label]	# the point in this part that connects another part
			label_connect_point = connect_list[c_label-1][label]	# the point in another part that connects this part
			shift_value = (label_connect_point[0] - c_connect_point[0], label_connect_point[1] - c_connect_point[1])
			shift_part(bold_parts, c_label, shift_value)
			adjust_connect_list(connect_list, c_label, label, shift_value)	# adjust the information of connecting points, 
																		# since the position has changed
			merge_parts(bold_parts, c_label, label)
			# new_connect_labels = new_connect_list[c_label-1]
			# adjust_connect_parts(bold_parts, connect_list, new_connect_labels, shift_value)
			# new_connect_list[label-1].append(c_label)
			break

	min_h, min_w = 1000, 1000
	max_h, max_w = -1000, -1000

	for part in bold_parts:
		if (len(part) <= 0):
			continue
		r, c = np.array(part).T
		min_h = min(min_h, min(r))
		min_w = min(min_w, min(c))
		max_h = max(max_h, max(r))
		max_w = max(max_w, max(c))
	h = max_h - min_h + 1
	w = max_w - min_w + 1
	# print(h, w)
	# method 1
	out_img = np.zeros([h, w])
	out_img.fill(255)

	ori_img = np.zeros([h, w])
	ori_img.fill(-1)
	n = 0
	for part in bold_parts:
		if (len(part) <= 0):
			continue
		r, c = np.array(part).T
		r -= min_h
		c -= min_w
		out_img[r, c] = 0
		ori = aver_orientation[n]
		ori_img[r, c] = ori

	extend = 10
	h += extend * 2
	w += extend * 2

	ext_out_img = np.zeros([h, w])
	ext_out_img.fill(255)
	ext_out_img[extend:h-extend, extend:w-extend] = out_img

	ext_ori_img = np.zeros([h, w])
	ext_ori_img.fill(-1)
	ext_ori_img[extend:h-extend, extend:w-extend] = ori_img

	
	return ext_out_img, ext_ori_img
import numpy as np
from modules import extension as ext
import math

def in_range(the_range, orient):
	if (orient >= the_range[0] and orient <= the_range[1]):
		return True
	else:
		return False


def check_around(cut_point_img, point, p=3):
	h, w = cut_point_img.shape
	r, c = point
	left_r, right_r = max(0, r-p), min(h-1, r+p)
	left_c, right_c = max(0, c-p), min(w-1, c+p)
	for i in range(left_r, right_r+1):
		for j in range(left_c, right_c+1):
			if (i, j) == point:
				# print("== point")
				continue
			if cut_point_img[i, j] == 1:
				return True
	return False

def check_around_2(img, cut_point_img, point, p=1):
	h, w = cut_point_img.shape
	r, c = point
	left_r, right_r = max(0, r-p), min(h-1, r+p)
	left_c, right_c = max(0, c-p), min(w-1, c+p)
	for i in range(left_r, right_r+1):
		for j in range(left_c, right_c+1):
			p = (i, j)
			if (img[p] > 0):
				continue
			if cut_point_img[p] == 0:
				return True # there is a non-cut_point around it
	return False

def check_around_3(cut_point_img, cut_point, point, p=1):
	# check if there is a cut_point which is not cut_point above around it
	h, w = cut_point_img.shape
	r, c = point
	left_r, right_r = max(0, r-p), min(h-1, r+p)
	left_c, right_c = max(0, c-p), min(w-1, c+p)
	for i in range(left_r, right_r+1):
		for j in range(left_c, right_c+1):
			current_p = (i, j)
			if current_p == point or current_p == cut_point:
				continue
			if cut_point_img[current_p] == 1:
				# print("point: ", point, ", cut_point: ", cut_point, ", another cut_point: ", current_p)
				return current_p
	return None

def get_range(orient_value, threshold):
	range_1 = np.array([orient_value - threshold/2, orient_value + threshold / 2]) % 360
	range_2 = (range_1 + 180) % 360
	if range_1[0] > 180:
		range_1[0] = 0
	if range_1[1] > 180:
		range_1[1] = 180
	if (range_2 > 180).all():
		range_2 = range_1
	elif (range_2[1]-threshold/2 <= 0):
		range_2[0] = 0
	return range_1, range_2

def is_cut_point(cut_point_img, point, ext_orient, threshold):
	r, c = point
	orient_value = ext_orient[r+1][c+1]
	range_1, range_2 = get_range(orient_value, threshold)
	if (check_around(cut_point_img, point)):
		return False
	for i in range(r-1, r+2):
		for j in range(c-1, c+2):
			if (ext_orient[i+1, j+1] == -1):
				continue
			# if ((not in_range(range_1, ext_orient[i+1, j+1])) and (not in_range(range_2, ext_orient[i+1, j+1]))):
			if (get_orient_diff(orient_value, ext_orient[i+1, j+1]) > threshold):
				# print(ext_orient[i+1, j+1], " not in range of ", orient_value)
				return True
	return False


def add_around(cut_point_img, img, cut_points, point):
	h, w = cut_point_img.shape
	r, c = point
	left_r, right_r = max(0, r-1), min(h-1, r+1)
	left_c, right_c = max(0, c-1), min(w-1, c+1)
	add = 0
	last_point = point
	for i in range(left_r, right_r+1):
		for j in range(left_c, right_c+1):
			p = (i, j)
			if (p == point):
				continue
			if img[i, j] == 0:
				cut_point_img[i, j] = 1
				if (not p in cut_points):
					cut_points.append(p)
					add += 1
					last_point = p

def remove_all_cut_points_around(img, cut_point_img, cut_points):
	new_cut_points = cut_points.copy()
	for point in cut_points:
		if check_around_2(img, cut_point_img, point, 1):
			continue
		else:
			new_cut_points.remove(point)
			cut_point_img[point] = 0
			# print("remove!", point)
	return new_cut_points

def find_nearby(img, cut_point_img, point, p = 1):
	h, w = cut_point_img.shape
	r, c = point
	left_r, right_r = max(0, r-p), min(h-1, r+p)
	left_c, right_c = max(0, c-p), min(w-1, c+p)
	nearby_points = []
	for i in range(left_r, right_r+1):
		for j in range(left_c, right_c+1):
			current_p = (i, j)
			if (img[current_p] > 0 or current_p == point or cut_point_img[current_p] == 1):
				continue
			nearby_points.append(current_p)
	return nearby_points

def remove_overlap(img, cut_point_img, cut_points):
	new_cut_points = cut_points.copy()
	img_check = np.copy(img)
	for point in cut_points:
		nearby_points = find_nearby(img, cut_point_img, point, 2)
		# print(point, "nearby_points: ", nearby_points)
		to_remove = True
		for n_point in nearby_points:
			if check_around_3(cut_point_img, point, n_point, 2) == None:
				to_remove = False
				break
		if (to_remove):
			cut_point_img[point] = 0
			new_cut_points.remove(point)
	return new_cut_points

def same_dir(orient_1, orient_2):
	o1 = orient_1 - 90
	o2 = orient_2 - 90
	if abs(o1 - 0) < 10:
		o1 = 0
	if abs(o2 - 0) < 10:
		o2 = 0
	if o1 * o2 >= 0:
		return True
	return False

def find_next_pixel_2(parts, current_part, img_label, cut_point_img, cut_point, current_p, orientation, current_label, p=1, threshold=20):
	h, w = img_label.shape
	r, c = current_p
	left_r, right_r = max(0, r-p), min(h-1, r+p)
	left_c, right_c = max(0, c-p), min(w-1, c+p)

	points = []
	for i in range(left_r, right_r+1):
		for j in range(left_c, right_c+1):
			point = (i, j)
			if point == current_p or img_label[point] < 0:
				continue
			if (abs(i - cut_point[0]) >= 2 or abs(j - cut_point[1]) >= 2):
				connect_cut_point = check_around_3(cut_point_img, cut_point, point)
				if connect_cut_point != None:	# the point belongs to another cut point
					if (get_orient_diff(orientation[connect_cut_point], orientation[point]) < threshold) and same_dir(orientation[connect_cut_point], orientation[point]):
						continue
			if (img_label[point] > 0 and img_label[point] != current_label):
				old_part = parts[img_label[point]-1]
				old_aver_orient = count_orientation(old_part, orientation)
				current_orient = count_orientation(current_part, orientation)
				old_diff = get_orient_diff(old_aver_orient, orientation[point])
				diff = get_orient_diff(current_orient, orientation[point])
				if not (diff < old_diff and same_dir(current_orient, orientation[point])):	# change a point to a more proper part
					continue
				# print("current_label: ", current_label)
				# print("old_label: ", img_label[point])
				if (point in parts[img_label[point]-1]):
					parts[img_label[point]-1].remove(point)
			points.append(point)
	return points

def devide_parts(img, cut_point_img, cut_points, orientation):
	# parts = [part1, part2, part3, ...], is a list
	# part = [point1, point2, point3, ...], is a list
	h, w = img.shape
	img_label = np.where(img == 255, -1, 0)
	parts = []
	count = 1
	for point in cut_points:
		candidates = [point]
		part = []
		while(len(candidates) > 0):
			x_cur, y_cur = candidates[-1]
			candidates.pop()
			current_p = (x_cur, y_cur)
			if current_p in part:	# if the point has already in this part, continue
			    continue
			if current_p in cut_points and current_p != point:	# if find another cut point, continue (not to find this direction further)
			    continue
			part.append(current_p)	# add this point into the part
			if not current_p in cut_points:		# mark the non-cut-point as found
				img_label[current_p] = count

			# check if the 8 points around this point belongs to this part, and add them into this part if true
			next_pixel_pos = find_next_pixel_2(parts, part, img_label, cut_point_img, point, current_p, orientation, count)
			candidates += next_pixel_pos
		parts.append(part)
		count += 1
	if (len(parts) == 0):
		r, c = np.where(img == 0)
		part = list(zip(r, c))
		parts.append(part)
	return parts


def find_corresponding_part(cut_point, parts):
	for part in parts:
		if (part[0] == cut_point):
			return part
	return None

def get_orient_diff(orient_1, orient_2):
	max_orient = min(max(orient_1, orient_2), 180)
	min_orient = max(min(orient_1, orient_2), 0)
	diff = max_orient - min_orient
	diff_2 = (180 - max_orient) + min_orient
	diff = min(diff, diff_2)
	# if (diff >= 360):
	# 	print(diff)
	return diff

def get_label_connect(connect_list, c_label):
	connect_labels = []
	c_label_connect = list(connect_list[c_label-1])
	for label in c_label_connect:
		connect_labels.append(label)
	# print("1: ", connect_labels)
	for i in range(len(connect_list)):
		if (i == c_label-1):
			continue
		if (c_label in connect_list[i]):
			connect_labels.append(i+1)
	# print("2: ", connect_labels)
	return connect_labels

def merge_small_best(aver_orientation, cut_points, new_cut_points, cut_point, parts, best_part, c_part, connect_list, img_label, c_label, best_connect_label, orientation, least_num):
	connect_labels = get_label_connect(connect_list, c_label)
	# print("merge ", c_label, " to ", best_connect_label)
	to_merge_2(best_part, c_part)
	aver_orientation[best_connect_label-1] = count_orientation(best_part, orientation)
	new_cut_points.remove(cut_point)
	parts.remove(c_part)
	# print("remove label: ", c_label)
	for k in range(len(connect_labels)):
		connect_label = connect_labels[k]
		if (best_connect_label == connect_label):
			continue
		connect_cut_point = cut_points[connect_label-1]
		connect_part = find_corresponding_part(connect_cut_point, parts)
		if (connect_part == None or (not connect_cut_point in new_cut_points)):	# the part has been removed
			continue
		# print("in merge_small")
		merge_small(aver_orientation, cut_points, new_cut_points, connect_cut_point, parts, connect_part, connect_list, img_label, orientation, least_num, best_part, best_connect_label)

def merge_small(aver_orientation, cut_points, new_cut_points, cut_point, parts, c_part, connect_list, img_label, orientation, least_num, pre_merge_part=None, pre_merge_label=-1):
	if (len(c_part) < least_num):		# this size of this part is too small, merge with another part nearby
		c_label = img_label[cut_point]
		# c_label_connect = list(connect_list[c_label-1])
		connect_labels = get_label_connect(connect_list, c_label)
		c_aver_orient = aver_orientation[c_label-1]
		best_part = None
		best_connect_label = -1
		min_orient_diff = 360
		best_part_2 = None
		best_connect_label_2 = -1
		min_orient_diff_2 = 360
		if (pre_merge_part != None):
			best_part = pre_merge_part
			best_connect_label = pre_merge_label
			min_orient_diff = get_orient_diff(c_aver_orient, aver_orientation[pre_merge_label-1])
		# print(len(connect_labels))
		for i in range(len(connect_labels)):
			connect_label = connect_labels[i]
			connect_cut_point = cut_points[connect_label-1]
			connect_part = find_corresponding_part(connect_cut_point, parts)	# not accessing by index(label), since the part may has been removed
			if (connect_part == None or not connect_cut_point in new_cut_points):	# the part has been removed
				continue
			connect_aver_orient = aver_orientation[connect_label-1]		# original label, original aver_orientation, there is no mismatch
			orient_diff = get_orient_diff(c_aver_orient, connect_aver_orient)
			if (orient_diff < min_orient_diff):
				if same_dir(c_aver_orient, connect_aver_orient):
					best_part = connect_part
					best_connect_label = connect_label
					min_orient_diff = orient_diff
				else:
					best_part_2 = connect_part
					best_connect_label_2 = connect_label
					min_orient_diff_2 = orient_diff
		if (best_part != None):
			merge_small_best(aver_orientation, cut_points, new_cut_points, cut_point, parts, best_part, c_part, connect_list, img_label, c_label, best_connect_label, orientation, least_num)
		elif best_part_2 != None:
			merge_small_best(aver_orientation, cut_points, new_cut_points, cut_point, parts, best_part_2, c_part, connect_list, img_label, c_label, best_connect_label_2, orientation, least_num)
		else:
			print("pre_merge_label = ", pre_merge_label)
			print("best part is None :(")

def merge_parts(cut_points, parts, connect_list, img_label, orientation, least_num = 10):
	aver_orientation = get_aver_orientation(parts, orientation)
	new_cut_points = cut_points.copy()
	for cut_point in cut_points:
		c_part = find_corresponding_part(cut_point, parts)
		if (c_part == None):	# this part has been removed, remove this cut point
			if cut_point in new_cut_points:
				new_cut_points.remove(cut_point)
			continue
		merge_small(aver_orientation, cut_points, new_cut_points, cut_point, parts, c_part, connect_list, img_label, orientation, least_num)
	return new_cut_points, parts

def check_around_4(img_label, cut_point, count):
	h, w = img_label.shape
	r, c = cut_point
	left_r, right_r = max(0, r-count), min(h-1, r+count)
	left_c, right_c = max(0, c-count), min(w-1, c+count)
	c_label = img_label[cut_point]

	connect_points = []
	for i in range(left_r, right_r + 1):
		for j in range(left_c, right_c + 1):
			point = (i, j)
			label = img_label[point]
			if (label == 0 or label == c_label):
				continue
			connect_points.append(point)
	return connect_points

def connect_nearby_parts(cut_points, parts, img_label):
	connect_list = []
	for i in range(len(cut_points)):
		connect_list.append({})

	# find connect point around it
	for cut_point in cut_points:
		connected = False
		part = find_corresponding_part(cut_point, parts)
		c_label = img_label[cut_point]
		dic = connect_list[c_label - 1]
		for point in part:
			connect_points = check_around_4(img_label, point, 2)
			for p in connect_points:
				label = img_label[p]
				if (label in dic):
					connected = True
				elif (c_label in connect_list[label-1]):
					connected = True
				else:
					dic[label] = p
					connected = True
	return connect_list, parts

def to_label(img, parts):
	img_label = np.zeros_like(img)
	part_count = 1
	for part in parts:
		for point in part:
			if (img_label[point] != 0 and img_label[point] != part_count):
				part.remove(point)
			else:
				img_label[point] = part_count
		part_count += 1
	return img_label


def to_merge_2(part, connect_part):
	# merge connect_part into new_part
	# print("c_part: ", part)
	# print("connect_part: ", connect_part)
	for point in connect_part:
		if not point in part:
			part.append(point)

def find_part_index(cut_point, parts):
	for i in range(len(parts)):
		if (cut_point == parts[i][0]):
			return i
	return -1

def check_orientation(orient_1, orient_2, threshold):
	range_1, range_2 = get_range(orient_1, threshold)
	if in_range(range_1, orient_2) or in_range(range_2, orient_2):
		return True
	return False

def near_aver_orient(orient, aver):
	diff = get_orient_diff(orient, aver)
	new_orient = orient
	if (diff != abs(orient - aver)):
		new_orient = orient + 180
		if (new_orient < 270):
			new_orient += 360
		elif new_orient == 270:
			new_orient = 90
	return new_orient

def count_orientation(part, orientation):
	point_num = 0
	orientation_sum = 0
	# quad_1_count = 0
	# for point in part:
	# 	if (orientation[point] < 90):
	# 		quad_1_count += 1
	for point in part:
		orientation_sum += orientation[point]
		point_num += 1
	aver = orientation_sum / point_num

	point_num = 0
	orientation_sum = 0
	for point in part:
		new_orient = near_aver_orient(orientation[point], aver)
		if (abs(new_orient - aver) > 60):
			continue
		orientation_sum += new_orient
		point_num += 1
	aver = orientation_sum / point_num
	return aver

def get_aver_orientation(parts, orientation):
	aver_orientation = []
	for part in parts:
		aver = count_orientation(part, orientation)
		aver_orientation.append(aver)
	return aver_orientation

def merge_pwso(orientation, aver_orientation, cut_points, new_cut_points, connect_list, parts, c_part, c_label, threshold, pre_c_label=-1):
	connect_labels = get_label_connect(connect_list, c_label)
	aver_orient_label = c_label
	if (pre_c_label != -1):
		aver_orient_label = pre_c_label

	best_part = None
	min_diff = 360
	best_connect_label = -1
	for i in range(len(connect_labels)):
		connect_label = connect_labels[i]
		if (connect_label == pre_c_label):
			continue
		# connect_point = connect_list[c_label-1][connect_label]
		connect_cut_point = cut_points[connect_label-1]
		connect_part = find_corresponding_part(connect_cut_point, parts)	# don't find part by index, because some parts may has been removed
		if (connect_part == None or not connect_cut_point in new_cut_points):
			continue
		if (c_part == connect_part):
			# print("why:(((")
			continue
		c_aver_orient = aver_orientation[aver_orient_label-1]	# original label, original aver_orientation, there is no mismatch
		connect_aver_orient = aver_orientation[connect_label-1]
		diff = get_orient_diff(c_aver_orient, connect_aver_orient)
		if (diff < threshold and same_dir(c_aver_orient, connect_aver_orient)):
			if (diff < min_diff):
				min_diff = diff
				best_part = connect_part
				best_connect_label = connect_label
	if best_part != None:
		to_merge_2(c_part, best_part)
		aver_orientation[aver_orient_label-1] = count_orientation(c_part, orientation)
		new_cut_points.remove(cut_points[best_connect_label-1])
		parts.remove(best_part)
		merge_pwso(orientation, aver_orientation, cut_points, new_cut_points, connect_list, parts, c_part, best_connect_label, threshold, aver_orient_label)

def merge_parts_with_similar_orientation(cut_point_img, connect_list, img_label, cut_points, parts, orientation, threshold=30):
	aver_orientation = get_aver_orientation(parts, orientation)
	# print(aver_orientation)
	new_cut_points = cut_points.copy()
	n = 0
	for cut_point in cut_points:
		c_part = find_corresponding_part(cut_point, parts)
		if (c_part == None or (not cut_point in new_cut_points)):
			continue
		c_label = img_label[cut_point]
		merge_pwso(orientation, aver_orientation, cut_points, new_cut_points, connect_list, parts, c_part, c_label, threshold)
		n += 1
	return new_cut_points, parts

def adjust_orientation(img, orientation):
    h, w = img.shape
    for i in range(h):
        for j in range(w):
            if (img[i, j] == 0) and (orientation[i, j] < 0):
                orientation[i, j] += 180
    orientation[img == 255] = -1

def find_cut_point(img, orientation, threshold=45):
	cut_points = []
	h, w = img.shape

	adjust_orientation(img, orientation)
	ext_orient = ext.even_extension(orientation, 1)

	# find cut points
	r, c = np.where(img == 0) # background: white (255)
	cut_point_img = np.zeros_like(img)
	for i in range(r.size):
		point = (r[i], c[i])
		if (is_cut_point(cut_point_img, point, ext_orient, threshold)):
			cut_points.append(point)
			cut_point_img[point] = 1

	new_cut_points = cut_points.copy()
	for point in cut_points:
		if check_around(cut_point_img, point, 2):
			new_cut_points.remove(point)
			cut_point_img[point] = 0
	cut_point = new_cut_points
	new_cut_points = cut_point.copy()
	for point in cut_points:
		# print("before add, ", point, len(new_cut_points))
		add_around(cut_point_img, img, new_cut_points, point)
		# print("after add, ", point, len(new_cut_points))

	new_cut_points = remove_all_cut_points_around(img, cut_point_img, new_cut_points)
	new_cut_points = remove_overlap(img, cut_point_img, new_cut_points)

	parts = devide_parts(img, cut_point_img, new_cut_points, orientation)


	img_label = to_label(img, parts)
	connect_list, parts = connect_nearby_parts(new_cut_points, parts, img_label)
	new_cut_points, parts = merge_parts(new_cut_points, parts, connect_list, img_label, orientation)
	img_label = to_label(img, parts)
	connect_list, parts = connect_nearby_parts(new_cut_points, parts, img_label)
	new_cut_points, parts = merge_parts_with_similar_orientation(cut_point_img, connect_list, img_label, new_cut_points, parts, orientation)

	parts.sort(key=len, reverse=True)
	for i in range(len(parts)):
		new_cut_points[i] = parts[i][0]

	aver_orientation = get_aver_orientation(parts, orientation)
	# for i in range(len(aver_orientation)):
	# 	print(i+1, aver_orientation[i])
	img_label = to_label(img, parts)
	connect_list, parts = connect_nearby_parts(new_cut_points, parts, img_label)
	for i in range(len(connect_list)):
		connect_labels = list(connect_list[i])
		for label in connect_labels:
			point = connect_list[i][label]
			parts[i].append(point)
			# print("part ", i+1, ": append ", point, " from ", label)
			connect_list[label-1][i+1] = point
	# for i in range(len(connect_list)):
	# 	print(i+1, connect_list[i])

	return new_cut_points, parts, connect_list

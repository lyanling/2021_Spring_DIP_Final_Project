import numpy as np
from modules import extension as ext
import math

def in_range(the_range, orient):
	if (orient >= the_range[0] and orient <= the_range[1]):
		return True
	else:
		# print(the_range)
		# print(orient)
		return False

# def check(orient_1, orient_2):
# 	if (orient_1 == orient_2):
# 		return False

def is_cut_point(point, ext_orient, threshold):
	r, c = point
	orient_value = ext_orient[r+1][c+1]
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
	# print("orient = ", orient_value)
	# print("range_1 = ", range_1)
	# print("range_2 = ", range_2)
	
	for i in range(r-1, r+2):
		for j in range(c-1, c+2):
			if (ext_orient[i+1, j+1] == -1):
				continue
			if ((not in_range(range_1, ext_orient[i+1, j+1])) and (not in_range(range_2, ext_orient[i+1, j+1]))):
				# print(ext_orient[i+1, j+1], " not in range of ", orient_value)
				return True
	return False

def find_cut_point(img, orientation, threshold=150):
	cut_point = []

	h, w = orientation.shape
	r, c = np.where(img == 0) # background: white (255)
	
	orientation += 90
	orientation[img == 255] = -1
	ext_orient = ext.even_extension(orientation, 1)

	for i in range(r.size):
		point = [r[i], c[i]]
		if (is_cut_point(point, ext_orient, threshold)):
			cut_point.append(point)
	# print(len(cut_point))
	# print(r.size)
	return cut_point

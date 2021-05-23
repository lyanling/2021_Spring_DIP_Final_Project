import numpy as np
from modules import extension as ext
import math

def in_range(the_range, orient):
	if (orient >= the_range[0] and orient <= the_range[1]):
		return True
	else:
		return False

def is_cut_point(point, ext_orient, threshold):
	x, y = point
	orient_value = ext_orient[x+1][y+1]
	range_1 = np.array([orient_value - threshold/2, orient_value + threshold / 2]) % 360
	range_2 = (range_1 + 180) % 360
	if range_1[0] > 180:
		range_1[0] = 0
	if range_1[1] > 180:
		range_1[1] = 180
	if (range_2 > 180).all():
		range_2 = range_1
	
	for i in range(x-1, x+2):
		for j in range(y-1, y+2):
			if (in_range(range_1, ext_orient[i+1, j+1]) or in_range(range_2, ext_orient[i+1, j+1])):
				return True
	return False

def find_cut_point(img, orientation, threshold=60):
	cut_point = []

	h, w = orientation.shape
	x, y = np.where(img == 0) # background: white (255)
	
	orientation[(x, y)] += math.pi / 2
	orientation = orientation / math.pi * 180
	ext_orient = ext.even_extension(orientation, 1)

	for i in range(x.size):
		point = [x[i], y[i]]
		if (is_cut_point(point, ext_orient, threshold)):
			cut_point.append(point)

	return cut_point
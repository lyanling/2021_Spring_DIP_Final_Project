import numpy as np
from modules import extension as ext


def diff(a, b):
	return abs(a-b)

def is_cut_point(point, ext_orient, threshold):
	x, y = point
	for i in range(x-1, x+2):
		for j in range(y-1, y+2):
			if (diff(ext_orient[i+1, j+1], ext_orient[x+1, y+1]) > threshold):
				return True
	return False

def find_cut_point(img, orientation, threshold=10):
	cut_point = []

	h, w = orientation.shape
	ext_orient = ext.even_extension(orientation, 1)
	x, y = np.where(img == 0)
	for i in range(x.size):
		point = [x, y]
		if (is_cut_point(point, ext_orient, threshold)):
			cut_point.append(point)

	return cut_point
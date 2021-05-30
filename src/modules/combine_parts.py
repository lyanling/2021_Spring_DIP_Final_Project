import numpy as np
from ../ import orientation.get_orientation
from . import geo_modify as gm

def same_direction(theta_A, theta_B):
	return (theta_A*theta_B >= 0)

def points_equal()

def combine_parts(img, parts, connect_points):
	# parts: 
	# connect_points: [[part1's connect_points_pairs], [], [], ...]
	# part1's connect_points_pairs = [(X, part1's pointA, partX's point C), 
								# (Y, part1's point B, partY's point D), ...]

	out_img = np.zeros_like(img)
	for i in range(len(parts)):
		for p in parts[i]:
			out_img[p] = 255


	orientation = get_orientation(img)
	for i in range(len(parts)):
		for pairs in connect_points[i]:
			for pair in pairs:
				connect_part = pair[0]
				pointA = pair[1]
				pointB = pair[2]
				# dt = 1
				# step_1 = 2
				# step_2 = 4
				if (same_direction(orientation[pointA], pointB)):
					# smaller dt
					x, y = pointB - pointA
					dy = y / x
					pre_y = pointA[1]
					for xx in range(pointA[0]+1, pointB[0]):
						new_y = round(pre_y + dy)
						for yy in range(pre_y, new_y+1):
							out_img[xx, yy] = 255
						pre_y = new_y
	out_img = np.where[out_img == 255, 0, 255]
	return out_img


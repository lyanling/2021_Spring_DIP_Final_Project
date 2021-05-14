import numpy as np
import math

def to_cart(q, p, height):
	u = q - 0.5 # j
	v = height + 0.5 - p # i
	return (u, v)

def to_img_coord(u, v, height):
	q = u+0.5
	p = height + 0.5 - v
	return (p, q)

def bilinear_interpolation(img, point):
	r = point[0]
	c = point[1]
	if math.isnan(r):
		r = 0
	if math.isnan(c):
		c = 0
	p = int(r)
	q = int(c)
	if p < 0 or p >= img.shape[0] or q < 0 or q >= img.shape[1]:
		return 0
	p2 = p+1
	q2 = q+1
	if p2 >= img.shape[0]:
		p2 = p
	if q2 >= img.shape[1]:
		q2 = q
	a = r - p
	b = c - q
	f_point = (1-a)*(1-b)*img[p, q] + (1-a)*b*img[p, q2] + a*(1-b)*img[p2, q] + a*b*img[p2, q2]
	return f_point
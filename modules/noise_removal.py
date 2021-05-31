import numpy as np
from . import my_hist as mh
from . import extension as ext

			

def create_mask(mask, mask_type):
	my_mask = np.ones([mask, mask])
	if mask_type == 0:
		my_mask /= (mask * mask)
	elif mask_type == 1:
		mid = int(mask / 2)
		my_mask[mid, mid] = mid*2
		my_mask /= (my_mask.sum())
	else:
		mid = int(mask / 2)
		for i in range(mask):
			for j in range(mask):
				if i == mid or j == mid:
					my_mask[i, j] = 2 * mid
		my_mask[mid, mid] = (2*mid)**2
		my_mask /= my_mask.sum()
	return my_mask

def convolution(exten_img, my_mask, mask_size):
	s = 0
	for i in range(mask_size):
		for j in range(mask_size):
			s += (exten_img[i, j] * my_mask[i, j])
	return s

def low_pass(img, mask_size=3, extension=0, mask_type=2):
	periphery = int(mask_size / 2)
	img_r = img.shape[0]
	img_c = img.shape[1]
	if extension == 0:
		exten_img = ext.even_extension(img, periphery)
	else:
		exten_img = ext.odd_extension(img, periphery)
	my_mask = create_mask(mask_size, mask_type)
	new_img = np.zeros([img_r, img_c])
	for i in range(img_r):
		for j in range(img_c):
			new_img[i, j] = convolution(exten_img[i:i+mask_size, j:j+mask_size], my_mask, mask_size)
	return new_img


def detect(img, mask_size):
	a = np.zeros(mask_size*mask_size - 1)
	mid = int(mask_size / 2)
	count = 0
	for i in range(mask_size):
		for j in range(mask_size):
			if i == mid and j == mid:
				continue
			a[count] = img[i, j]
			count += 1
	std = np.std(a)
	aver = np.average(a)
	med = np.median(img)
	s = 0
	if abs(img[mid, mid] - aver) > std:
		return aver
	else:
		return img[mid, mid]


def outlier(img, mask_size=3, extension=0):
	periphery = int(mask_size / 2)
	img_r = img.shape[0]
	img_c = img.shape[1]
	if extension == 0:
		exten_img = ext.even_extension(img, periphery)
	else:
		exten_img = ext.odd_extension(img, periphery)
	new_img = np.zeros([img_r, img_c])
	for i in range(img_r):
		for j in range(img_c):
			new_img[i, j] = detect(exten_img[i:i+mask_size, j:j+mask_size], mask_size)
	return new_img

def median_filter(img, mask_size=3, extension=0):
	periphery = int(mask_size / 2)
	img_r = img.shape[0]
	img_c = img.shape[1]
	if extension == 0:
		exten_img = ext.even_extension(img, periphery)
	else:
		exten_img = exy.odd_extension(img, periphery)
	new_img = np.zeros([img_r, img_c])
	for i in range(img_r):
		for j in range(img_c):
			new_img[i, j] = np.median(exten_img[i:i+mask_size, j:j+mask_size])
	return new_img

def impulse_noise_rm(img, method=0, mask_size=3, extension=0):
	if method == 0:
		return median_filter(img, mask_size, extension)
	else:
		return outlier(img, mask_size, extension)

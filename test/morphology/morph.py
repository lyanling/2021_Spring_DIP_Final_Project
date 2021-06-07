import numpy as np

def erosion(img, H, mode='center'):
	H = H.astype(np.uint8)
	# if (mode == 'SER'):
	# 	H = H ^ 1
	h, w = img.shape
	new_img = np.zeros([h+2, w+2])
	new_img[1:h+1, 1:w+1] = img
	new_img = new_img.astype(np.uint8)
	t_img = np.zeros([h+2, w+2])
	for i in range(3):
		for j in range(3):
			t_img.fill(0)
			if H[i, j] == 1:
				t_img[i:i+h, j:j+w] = img
				t_img = t_img.astype(np.uint8)
				new_img &= t_img
	erosed_img = new_img[1:h+1, 1:w+1]
	return erosed_img

def dilation(img, H, mode='center'):
	H = H.astype(np.uint8)
	h, w = img.shape
	new_img = np.zeros([h+2, w+2])
	new_img[1:h+1, 1:w+1] = img
	new_img = new_img.astype(np.uint8)
	t_img = np.zeros_like(new_img)
	for i in range(3):
		for j in range(3):
			t_img.fill(0)
			if H[i, j] == 1:
				t_img[i:i+h, j:j+w] = img
				t_img = t_img.astype(np.uint8)
				new_img |= t_img
	dilated_img = new_img[1:h+1, 1:w+1]
	return dilated_img

def four_connected_nei(img):
	count = 0
	if img[1, 0] > 0:
		count += 1
	if img[0, 1] > 0:
		count += 1
	if img[2, 1] > 0:
		count += 1
	if img[1, 2] > 0:
		count += 1
	return count

def eight_connected_nei(img):
	count = 0
	if img[0, 0] > 0:
		count += 1
	if img[0, 2] > 0:
		count += 1
	if img[2, 0] > 0:
		count += 1
	if img[2, 2] > 0:
		count += 1
	return count

def cal_bond(img):
	h, w = img.shape
	ext_img = np.zeros([h+2, w+2])
	ext_img[1:h+1, 1:w+1] = img
	img_bond = np.zeros_like(img)

	for i in range(h):
		for j in range(w):
			if (ext_img[i+1, j+1] == 0):
				continue
			else:
				img_bond[i, j] += (four_connected_nei(ext_img[i:i+3, j:j+3]) * 2)
				img_bond[i, j] += eight_connected_nei(ext_img[i:i+3, j:j+3])
	return img_bond
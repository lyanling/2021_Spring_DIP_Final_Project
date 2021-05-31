import numpy as np
from . import to_cdf as tc
from . import my_hist as mh
from . import extension as ext

def find_x(aver, prob):
	for i in range(256):
		if prob <= (aver * i):
			break
	return i

def transfer_func(img, hist):
	s = sum(hist)
	aver_prob = (s / 256) / s
	pdf = hist / s
	cdf = tc.to_cdf(pdf)
	color_match = np.zeros(256)
	for i in range(256):
		color_match[i] = find_x(aver_prob, cdf[i])
	e_img = np.zeros([img.shape[0], img.shape[1]])
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			e_img[i, j] = color_match[img[i, j]]
	return e_img


def enhance_trans(img, local=0, window_size=128, enhance_area=110, move=8, extension=0):
	if not local:
		hist = mh.my_hist(img)
		return transfer_func(img, hist)
	periphery = int((window_size - enhance_area) / 2)
	c = 0
	r = 0
	max_r = img.shape[0]
	max_c = img.shape[1]
	img_6 = np.zeros([max_r, max_c])
	if extension == 0:
		while (r + window_size <= max_r):
			c = 0
			while (c + window_size <= max_c):
				hist = mh.my_hist(img[r:r+window_size, c:c+window_size])
				local_img = transfer_func(img[r:r+window_size, c:c+window_size], hist)
				if ((r*c == 0) or (r+window_size == max_r) or (c+window_size == max_c)):
					img_6[r:r+window_size, c:c+window_size] = local_img
				else:
					r2 = r + periphery
					c2 = c + periphery
					img_6[r2:r2+enhance_area, c2:c2+enhance_area] = local_img[periphery:periphery+enhance_area, periphery:periphery+enhance_area]
				if (c + window_size < max_c):
					c += move
					if (c + window_size >= max_c):
						c = max_c - window_size
				else:
					break
			if (r + window_size < max_r):
					r += move
					if (r + window_size >= max_r):
						r = max_r - window_size
			else:
				break
	# elif extension == 0 and direction == 1:
	# 	while (r + window_size <= max_r):
	# 		c = max_c - 1
	# 		while (c - window_size + 1 >= 0):
	# 			hist = mh.my_hist(img[r:r+window_size, c-window_size+1:c+1])
	# 			local_img = transfer_func(img[r:r+window_size, c-window_size+1:c+1], hist)
	# 			if ((r*(c-window_size+1) == 0) or (r+window_size == max_r) or (c == max_c-1)):
	# 				img_6[r:r+window_size, c-window_size+1:c+1] = local_img
	# 			else:
	# 				r2 = r + periphery
	# 				c2 = c - periphery
	# 				img_6[r2:r2+enhance_area, c2-enhance_area+1:c2+1] = local_img[periphery:periphery+enhance_area, periphery:periphery+enhance_area]
	# 			if (c - window_size + 1 > 0):
	# 				c -= move
	# 				if (c - window_size + 1 < 0):
	# 					c = window_size-1
	# 			else:
	# 				break
	# 		if (r + window_size < max_r):
	# 				r += move
	# 				if (r + window_size >= max_r):
	# 					r = max_r - window_size
	# 		else:
	# 			break
	else:
		p = int((window_size - enhance_area)/2)
		ext_img = ext.aver_extension(img, p)
		ext_img = ext_img.astype(np.uint8)
		e_max_r = ext_img.shape[0]
		e_max_c = ext_img.shape[1]
		new_ext_img = np.zeros([e_max_r, e_max_c])
		while (r + window_size <= e_max_r):
			c = 0
			while (c + window_size <= e_max_c):
				hist = mh.my_hist(ext_img[r:r+window_size, c:c+window_size])
				local_img = transfer_func(ext_img[r:r+window_size, c:c+window_size], hist)
				r2 = r + periphery
				c2 = c + periphery
				new_ext_img[r2:r2+enhance_area, c2:c2+enhance_area] = local_img[periphery:periphery+enhance_area, periphery:periphery+enhance_area]
				if (c + window_size < e_max_c):
					c += move
					if (c + window_size >= e_max_c):
						c = e_max_c - window_size
				else:
					break
			if (r + window_size < e_max_r):
					r += move
					if (r + window_size >= e_max_r):
						r = e_max_r - window_size
			else:
				break
		img_6 = new_ext_img[p:p+max_r, p:p+max_c]
	return img_6
import numpy as np


def my_hist(img):
	y = np.zeros(256)
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			y[img[i, j]] += 1
	return y
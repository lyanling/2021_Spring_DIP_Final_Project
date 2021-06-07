import numpy as np


def even_extension(img, periphery):
	img_r = img.shape[0]
	img_c = img.shape[1]
	exten_img = np.zeros([img_r+2*periphery, img_c+2*periphery])
	exten_img[periphery:periphery+img_r, periphery:periphery+img_c] = img
	for i in range(0, periphery):
		for j in range(exten_img.shape[1]):
			if j < periphery:
				exten_img[i, j] = exten_img[periphery, periphery]
			elif j >= periphery+img_c:
				exten_img[i, j] = exten_img[periphery, img_c+periphery-1]
			else:
				exten_img[i, j] = exten_img[periphery, j]
	for i in range(img_r+periphery, img_r+2*periphery):
		for j in range(exten_img.shape[1]):
			if j < periphery:
				exten_img[i, j] = exten_img[periphery+img_r-1, periphery]
			elif j >= periphery+img_c:
				exten_img[i, j] = exten_img[periphery+img_r-1, img_c+periphery-1]
			else:
				exten_img[i, j] = exten_img[periphery+img_r-1, j]
	for j in range(0, periphery):
		for i in range(periphery, img_r+periphery):
			exten_img[i, j] = exten_img[i, periphery]
	for j in range(img_c+periphery, img_c+periphery*2):
		for i in range(periphery, img_r+periphery):
			exten_img[i, j] = exten_img[i, img_c+periphery-1]
	return exten_img

def odd_extension(img, periphery):
	img_r = img.shape[0]
	img_c = img.shape[1]
	exten_img = np.zeros([img_r+2*periphery, img_c+2*periphery])
	exten_img[periphery:periphery+img_r, periphery:periphery+img_c] = img
	for i in range(0, periphery):
		for j in range(exten_img.shape[1]):
			if j < periphery:
				c=periphery
			elif j >= periphery+img_c:
				c = img_c+periphery-1
			else:
				c = j
			v = np.array([periphery, c]) - np.array([i, j])
			exten_img[i, j] = exten_img[i+v[0]*2, j+v[1]*2]
	for i in range(periphery+img_r, periphery*2+img_r):
		for j in range(exten_img.shape[1]):
			if j < periphery:
				c=periphery
			elif j >= periphery+img_c:
				c = img_c+periphery-1
			else:
				c = j
			v = np.array([img_r+periphery-1, c]) - np.array([i, j])
			exten_img[i, j] = exten_img[i+v[0]*2, j+v[1]*2]
	for j in range(0, periphery):
		for i in range(periphery, img_r+periphery):
			r = i
			v = np.array([r, periphery]) - np.array([i, j])
			exten_img[i, j] = exten_img[i+v[0]*2, j+v[1]*2]
	for j in range(periphery+img_c, periphery*2+img_c):
		for i in range(periphery, img_r+periphery):
			r = i
			v = np.array([r, periphery+img_c-1]) - np.array([i, j])
			exten_img[i, j] = exten_img[i+v[0]*2, j+v[1]*2]
	return exten_img


def aver_extension(img, periphery):
	img_r = img.shape[0]
	img_c = img.shape[1]
	exten_img = np.zeros([img_r+2*periphery, img_c+2*periphery])
	exten_img[periphery:periphery+img_r, periphery:periphery+img_c] = img
	aver = np.average(img)
	aver_r = 255/2 - (aver - 255/2)
	for i in range(0, periphery):
		for j in range(exten_img.shape[1]):
			exten_img[i, j] = aver_r
	for i in range(img_r+periphery, img_r+2*periphery):
		for j in range(exten_img.shape[1]):
			exten_img[i, j] = 255/2
	for j in range(0, periphery):
		for i in range(periphery, img_r+periphery):
			exten_img[i, j] = 255/2
	for j in range(0, periphery):
		for i in range(periphery, img_r+periphery):
			exten_img[i, j] = 255/2
	return exten_img
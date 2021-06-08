import numpy as np

def changeColor(img, color='black'):
	if color == 'black':
		return img
	rgb = np.array[0, 0, 0]
	if  color == 'red':
		rgb[0] = 255
	elif color == 'green':
		rgb[1] = 255
	else:
		rgb[2] = 255
	h, w = img.shape
	c = 3

	rgb_img = np.zeros([h, w, c])
	i, j = np.where(img == 0)
	rgb_img[i, j, ] = rgb

	return rgb_img

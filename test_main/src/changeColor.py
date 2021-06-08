import numpy as np

def changeColor(img, color='black'):
	rgb = np.array([0, 0, 0])
	if  color == 'red':
		rgb[2] = 255
	elif color == 'green':
		rgb[1] = 255
	elif color == 'blue':
		rgb[0] = 255
	
	h, w = img.shape
	c = 3

	rgb_img = np.zeros([h, w, c])
	rgb_img.fill(255)
	i, j = np.where(img == 0)
	rgb_img[i, j, ] = rgb

	return rgb_img

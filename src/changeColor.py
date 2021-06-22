import numpy as np
import webcolors

def changeColor(img, color='black'):
	rgb = np.array([0, 0, 0])
	rgb_tri = webcolors.name_to_rgb(color)
	rgb[0] = rgb_tri[2]
	rgb[1] = rgb_tri[1]
	rgb[2] = rgb_tri[0]
	h, w = img.shape
	c = 3

	rgb_img = np.zeros([h, w, c])
	rgb_img.fill(255)
	i, j = np.where(img == 0)
	rgb_img[i, j, ] = rgb

	return rgb_img

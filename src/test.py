import sys, getopt
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import morphology.thinning as thin
import morphology.skeletonize as sk
import morphology.morph as morph
from numpy.linalg import inv
import modules.geo_modify as gm


inputfile1 = 'sample.jpg'
outputfile = 'thin_sample.jpg'

def save_img(img_array, img_name):
	img = Image.fromarray(img_array)
	img.save(img_name)

origin_img = Image.open(inputfile1)
img = np.asarray(origin_img)
print(img.shape)
if (len(img.shape) > 2):
	img = img[:, :, 0]
	img = np.reshape(img, [img.shape[0], img.shape[1]])
print(img.shape)

height, width = img.shape
# print(np.max(img))
# img = img[:, :, 0]

print(np.max(img))
print(np.min(img))

gray_img = np.zeros(img.shape)
gray_img[img >= 100] = 255
gray_img[img <= 100] = 0
gray_img = gray_img.astype(np.uint8)
save_img(gray_img, "tmp.png")

# scaling
scale_mag = 1
S = np.array([[scale_mag, 0, 0], [0, scale_mag, 0], [0, 0, 1]])
M = S
M_inv = inv(M)

new_img = np.zeros([height, width])
for i in range(height):
	for j in range(width):
		(x, y) = gm.to_cart(j, i, height)
		in_vec = np.array([x, y, 1])
		u, v, z = M_inv.dot(in_vec)
		c_point = gm.to_img_coord(u, v, height)
		new_img[i, j] = gm.bilinear_interpolation(gray_img, c_point)

h = int(height*scale_mag)
w = int(width*scale_mag)
scale_img = new_img[height-h:, :w]
scale_img2 = np.zeros_like(scale_img)
scale_img2[scale_img >= 100] = 255
scale_img2[scale_img < 100] = 0

# scale_img2 = scale_img2.astype(np.uint8)
# save_img(scale_img2, outputfile)


r_img = thin.thinning(scale_img)
r_img = r_img.astype(np.uint8)
save_img(r_img, outputfile)
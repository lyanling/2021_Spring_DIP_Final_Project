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


inputfile1 = 'out.jpg'
outputfile = 'bold.jpg'

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

gray_img = np.zeros(img.shape)
gray_img[img >= 100] = 255
gray_img[img <= 100] = 0
gray_img = gray_img.astype(np.uint8)

r_img = morph.dilation(gray_img, np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]))
r_img = r_img.astype(np.uint8)
save_img(r_img, outputfile)
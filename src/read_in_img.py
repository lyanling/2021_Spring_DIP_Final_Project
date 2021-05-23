import sys, getopt
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import modules.enhance_trans as ent
import morphology.morph as morph
import morphology.thinning as thin

inputfile1 = '../samples/A_origin.jpg'
outputfile = '../out/A_origin_out.jpg'

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

out_img = np.zeros_like(img)

# img = 255 - img

# img = img // 10
# img = img * 10
# img = 255 - img

# out_img = ent.enhance_trans(img)

out_img[img > 100] = 255
out_img[img <= 100] = 0

out_img = 255 - out_img

# out_img = morph.dilation(out_img, np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]))


out_img = out_img.astype(np.uint8)


save_img(out_img, outputfile)


r_img = thin.thinning(out_img)
out_img = 255 - out_img

r_img = r_img.astype(np.uint8)
save_img(r_img, "../out/A_thin.jpg")
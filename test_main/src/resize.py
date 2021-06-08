import numpy as np
import transformation as trans
from modules import geo_modify as gm
import bounding_box as box

def resize(img, bottom_line, size=12):
	h, w = img.shape
	extend = 20
	h += extend*2
	w += extend*2

	ext_img = np.zeros([h, w])
    ext_img.fill(255)
    ext_img[extend:h-extend, extend:w-extend] = img

    part_idx = np.where(ext_img==0)
    max_x, min_x, max_y, min_y = part_idx[0].max(), part_idx[0].min(), part_idx[1].max(), part_idx[1].min()
    center_x = (max_x+min_x)//2
    center_y = (max_y+min_y)//2
    center = (center_x, center_y)  # center at the point with smallest r
    cart_center = gm.to_cart(center[1], center[0], h)   # to cartesian coordinate

    M, trans_img, dt = backward_transformation(ext_img, cart_center, mode="resize", size=size)
    scale_mag = 1 / 36 * size

    (h1, h2, w1, w2), tmp_bottom_line = box.get_bounding_box(word)
    bound_img = trans_img[h1:h2+1, w1:w2+1]
    new_bottom_line = int(bottom_line * scale_mag)

    return bound_img, new_bottom_line
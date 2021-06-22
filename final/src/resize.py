import numpy as np
import transformation as trans
from modules import geo_modify as gm

def resize(img, bottom_line, size=12):
    h, w = img.shape
    # print(h, w)
    extend = max(round(np.ceil(size/36) * max(h, w) / 2), 0)
    h += extend*2
    w += extend*2
    ext_img = np.zeros([h, w])
    ext_img.fill(255)
    ext_img[extend:h-extend, extend:w-extend] = img
    center_x = h//2
    center_y = w//2
    center = (center_x, center_y)  # center at the point with smallest r
    cart_center = gm.to_cart(center[1], center[0], h)   # to cartesian coordinate

    M, trans_img, dt = trans.backward_transformation(ext_img, cart_center, mode="resize", size=size)
    scale_mag = 1 / 36 * size

    new_bottom_line = int(bottom_line * scale_mag)

    return trans_img, new_bottom_line
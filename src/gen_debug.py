from pathlib import Path
import cv2 as cv
import numpy as np

def save_trans_parts(img, i, parts):
    part_dir = 'trans_parts/'
    Path(part_dir).mkdir(parents=True, exist_ok=True)
    n = 0
    h, w = img.shape
    for part in parts:
        part_img_name = part_dir+str(i)+'_'+str(n)+'.png'
        part_img = np.zeros_like(img)
        part_img = np.full(part_img.shape, 255)
        for point in part:
            if point[0] < 0 or point[0] >= h or point[1] < 0 or point[1] >= w:
                continue
            part_img[tuple(point)] = 0
        cv.imwrite(part_img_name, part_img.astype(np.uint8))
        n += 1
    return 

def save_combine_img(img, i):
    path_dir = 'combine_imgs/'
    Path(path_dir).mkdir(parents=True, exist_ok=True)
    file_name = path_dir + str(i) + '.png'
    cv.imwrite(file_name, img)
    return 
import cv2 as cv
import numpy as np
from pathlib import Path
import morphology.thinning as thin

def inv(img):
    full_img = np.full(img.shape, 255)
    return full_img-img

def get_bounding_box(word):
    # boundary
    word_locs = np.argwhere(word==0)
    if word_locs.size == 0:
        return word, None
    h1, w1 = word_locs.min(axis = 0)
    h2, w2 = word_locs.max(axis = 0)
    # bounding box
    word_bobox = word[h1:h2+1, w1:w2+1]
    # bottom line
    bottom_line = int(word.shape[0]*(2/3)-h1)
    return word_bobox, bottom_line

def get_thinning_box(in_path, out_path, start_idx=33, end_idx=38):
    thin_dir = Path(f'{out_path}/thinning')
    thin_dir.mkdir(parents=True, exist_ok=True)
    for i in range(start_idx, end_idx+1):
        word = cv.imread(f'{in_path}/{i}.png', cv.IMREAD_GRAYSCALE)
        thin_word = inv(thin.thinning(inv(word)))
        cv.imwrite(f'{thin_dir}/{i}.png', thin_word)
    return str(thin_dir)

def get_bottom_line(file_dir):
    bottom_line = []
    with open(file_dir+'/bottom_line.txt', 'r') as f:
        bottom_line = [int(l.rstrip()) for l in f.readlines()]
    return(bottom_line)
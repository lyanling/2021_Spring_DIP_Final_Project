import cv2
import numpy as np
from pathlib import Path
import morphology.thinning as thin

def inv(img):
    full_img = np.full(img.shape, 255)
    return full_img-img

def get_bounding_box(file_dir, start_idx=33, end_idx=126):
    new_dir = file_dir+'_box/'
    Path(new_dir).mkdir(parents=True, exist_ok=True)
    bottom_line = []
    
    for idx in range(start_idx, end_idx+1):  # ASCII:33~126
        word = cv2.imread(file_dir+'/'+str(idx)+'.png', cv2.IMREAD_GRAYSCALE)
        thin_word = thin.thinning(word)
        # boundary
        word_locs = np.argwhere(thin_word==0)
        h1, w1 = word_locs.min(axis = 0)
        h2, w2 = word_locs.max(axis = 0)
        # bounding box
        word_bobox = thin_word[h1:h2+1, w1:w2+1]
        cv2.imwrite(new_dir+str(idx)+'.png', word_bobox)
        # bottom line
        bottom_line.append(int(word.shape[0]*(2/3)-h1))

    with open(new_dir+"bottom_line.txt", "w") as f:
        f.writelines("%s\n" % l for l in bottom_line)    
    return new_dir

def get_bottom_line(file_dir):
    bottom_line = []
    with open(file_dir+'_box/bottom_line.txt', 'r') as f:
        bottom_line = [int(l.rstrip()) for l in f.readlines()]
    return(bottom_line)



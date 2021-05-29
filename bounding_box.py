import cv2
import numpy as np
from pathlib import Path

def get_bounding_box(file_dir, start_idx=33, end_idx=126):
    new_dir = file_dir+'_box'
    Path(new_dir).mkdir(parents=True, exist_ok=True)
    for idx in range(33, 127):  # ASCII:33~126
        word = cv2.imread(file_dir+'/'+str(idx)+'.png', cv2.IMREAD_GRAYSCALE)
        # boundary
        word_locs = np.argwhere(word==0)
        h1, w1 = word_locs.min(axis = 0)
        h2, w2 = word_locs.max(axis = 0)
        # bounding box
        word_bobox = word[h1:h2+1, w1:w2+1]
        cv2.imwrite(new_dir+'/'+str(idx)+'.png', word_bobox)
    return

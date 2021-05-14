import cv2
import numpy as np
import os

def bounding_box(file_dir):
    pic_num = 1
    new_dir = file_dir+'_box'
    os.mkdir(new_dir)
    for idx in range(pic_num):
        word = cv2.imread(file_dir+'/'+str(idx)+'.jpg', cv2.IMREAD_GRAYSCALE)
        word_locs = np.argwhere(word==0)
        h1, w1 = word_locs.min(axis = 0)
        h2, w2 = word_locs.max(axis = 0)
        word_bobox = word[h1:h2, w1:w2]
        cv2.imwrite(new_dir+'/'+str(idx)+'.jpg', word_bobox)
    return





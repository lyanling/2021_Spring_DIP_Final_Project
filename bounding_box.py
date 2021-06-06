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
        thin_word = inv(thin.thinning(inv(word)))
        # boundary
        word_locs = np.argwhere(thin_word==0)
        h1, w1 = word_locs.min(axis = 0)
        h2, w2 = word_locs.max(axis = 0)
        # bounding box
        word_bobox = thin_word[h1:h2+1, w1:w2+1]
        cv2.imwrite(new_dir+str(idx)+'.png', word_bobox)
        # bottom line
        bottom_line.append([idx, int(word.shape[0]*(2/3)-h1)])
    
    with open(new_dir+"bottom_line.txt", "w") as f:
        f.writelines(str(l[0])+' '+str(l[1])+'\n' for l in bottom_line)    
    return new_dir

def get_bottom_line(file_dir):
    bottom_line = []
    with open(file_dir+'/bottom_line.txt', 'r') as f:
        bottom_line = [l.split() for l in f.readlines()]
    d = dict()
    for bm in bottom_line:
        d[int(bm[0])] = int(bm[1])
    return d


def get_combined_bottom_line(img, idx, file_dir):
    bottom_line = get_bottom_line(file_dir)
    old = cv2.imread(file_dir+'/'+str(idx)+'.png', cv2.IMREAD_GRAYSCALE)
    new_bottom_line = int(bottom_line[idx]+(img.shape[0]/2-old.shape[0]/2))
    return new_bottom_line

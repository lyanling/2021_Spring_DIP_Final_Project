import numpy as np
import cv2 as cv
from pathlib import Path
import pickle

def classify(img, label_thin):
    m, n = img.shape
    label_img = label_thin.copy()
    last = np.array(np.where(label_thin > 0))
    new = np.zeros_like(label_thin)
    while(True):
        if last[0].size == 0:
            break
        last = last.T
        for i in range(last.shape[0]):
            center = tuple(last[i])
            x_m, x_M, y_m, y_M = max(0, center[0]-1), min(m-1, center[0]+1), max(0, center[1]-1), min(n-1, center[1]+1)
            mask_img = img[x_m:x_M+1, y_m:y_M+1]
            mask_label = label_img[x_m:x_M+1, y_m:y_M+1]
            mask = mask_img + mask_label
            mask = np.where(mask == 0, label_img[center], 0)
            label_img[x_m:x_M+1, y_m:y_M+1] += mask
            new[x_m:x_M+1, y_m:y_M+1] += mask
        last = np.array(np.where(new > 0))
        new = np.zeros_like(label_thin)
    return label_img

def classify_all(dir_frame, dir_label):
    Path(f"./full_label").mkdir(parents=True, exist_ok=True)
    for i in range(33, 127):
        frame_name = f'{i}.png'
        img = cv.imread(dir_frame+frame_name, cv.IMREAD_GRAYSCALE)
        label = cv.imread(dir_label+frame_name, cv.IMREAD_GRAYSCALE)
        full_label = classify(img, label)
        full_label_img = (full_label * (255 / full_label.max())).astype(np.uint8)
        cv.imwrite(f'./full_label/{i}_check.png', full_label_img)
        with open(f'./full_label/{i}.pickle', 'wb') as fout:
            pickle.dump(full_label, fout)
    return
import numpy as np
import cv2 as cv
from pathlib import Path
import pickle

def classify(img, label_thin):
    label_img = label_thin.copy()
    # use dilation
    kernel = np.ones((3, 3))
    count = label_img.max()
    while(True):
        fin = 0
        for i in range(1, count+1):
            label_part = np.where(label_img == i, 255, 0).astype(np.uint8)
            dilated = cv.dilate(label_part, kernel, iterations=1)
            dilated = np.where(dilated == 255)
            mask = img[dilated] + label_img[dilated]
            mask = np.where(mask == 0, i, 0).astype(np.uint8)
            label_img[dilated] += mask
            if (mask == 0).all():
                fin += 1
        if fin == count:
            break
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
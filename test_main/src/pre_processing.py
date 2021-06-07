import numpy as np
import cv2 as cv
from pathlib import Path
import bounding_box as box
import time



def object_counting(img):
    contours, _ = cv.findContours(img.astype(np.uint8), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    count = len(contours)
    label = np.zeros_like(img)
    for (i, cnt) in enumerate(contours):
        cv.drawContours(label, [cnt], 0, i+1, thickness=-1)
    return count, label

def thresholding(img, t):
    img_bool = np.where(img > t, False, True)   # pattern be True
    img_uint8 = np.where(img > t, 0, 255).astype(np.uint8)  # whilte pattern 
    img_check = np.where(img > t, 255, 0).astype(np.uint8)  # black pattern
    return img_bool, img_uint8, img_check

def cleanBoundary(img, img_bool, manual=False, width=6):
    m, n = img.shape
    last_s = 0
    for i in range(m):
        pos = np.where(img_bool[i] == True)
        s = pos[0].size
        if (s == 0 or (s == last_s and s < n/3)) and i > 3: break
        else:
            img[i][:] = 255
            img_bool[i][:] = False
            last_s = s
    last_s = 0
    for i in range(m-1, -1, -1):
        pos = np.where(img_bool[i] == True)
        s = pos[0].size
        if (s == 0 or (s == last_s and s < n/3)) and i < m-4: break
        else:
            img[i][:] = 255
            img_bool[i][:] = False
            last_s = s
    img = img.T
    img_bool = img_bool.T
    last_s = 0
    for i in range(n):
        pos = np.where(img_bool[i] == True)
        s = pos[0].size
        if (s == 0 or (s == last_s and s < m/3)) and i > 3: break
        else:
            img[i][:] = 255
            img_bool[i][:] = False
            last_s = s
    last_s = 0
    for i in range(n-1, -1, -1):
        pos = np.where(img_bool[i] == True)
        s = pos[0].size
        if (s == 0 or (s == last_s and s < m/3)) and i < n-4: break
        else:
            img[i][:] = 255
            img_bool[i][:] = False
            last_s = s
    img = img.T
    img_bool = img_bool.T
    return img, img_bool

def extractFrames(img, label, count, img_bool, start_ascii_code, out_path):
    x, y = [], [] # the upper-left corner of each frame
    error_count = 0
    bottom_line_list = []
    for i in range(1, count+1):
        I = np.where(label == i)
        if I[0].size < 30000:
            label[I] = 0
            error_count += 1
            print(i)
            continue
        label[I] = i - error_count
        x.append(I[0].min())
        y.append(I[1].min())
    x, y = np.array(x), np.array(y)
    ind = np.argsort(x)
    rows_i = [ind[i*3:(i+1)*3] for i in range(2)]
    rows = [y[rows_i[i]] for i in range(2)]
    sort_ind = np.zeros((1, 0), dtype=int)
    for i in range(len(rows)):
        r = (rows_i[i][np.argsort(rows[i])]).astype(int).reshape((1, -1))
        sort_ind = np.concatenate((sort_ind, r), axis=1)
    sort_ind = sort_ind.flatten()
    count -= error_count
    for i in range(count):
        I = np.where(label == sort_ind[i] + 1)
        x_max, x_min, y_max, y_min = I[0].max(), I[0].min(), I[1].max(), I[1].min()
        frame = np.zeros((x_max-x_min+1, y_max-y_min+1), dtype=np.uint8)
        frame_bool = np.zeros((x_max-x_min+1, y_max-y_min+1), dtype=bool)
        I_frame = tuple([I[0] - x_min, I[1]-y_min])
        frame[I_frame] = img[I]
        frame_bool[I_frame] = img_bool[I]
        frame, frame_bool = cleanBoundary(frame, frame_bool)
        # closing
        frame = np.where(frame==0, 255, 0).astype(np.uint8)
        frame = cv.morphologyEx(frame, cv.MORPH_CLOSE, np.ones((5, 5)))
        # opening
        frame = cv.morphologyEx(frame, cv.MORPH_OPEN, np.ones((3, 3)))
        thin_frame = cv.ximgproc.thinning(frame)
        frame = np.where(frame==0, 255, 0).astype(np.uint8)
        thin_frame = np.where(thin_frame==0, 255, 0).astype(np.uint8)
        bound, bottom_line = box.get_bounding_box(frame)
        if bound is not None:
            h1, h2, w1, w2 = bound
            bounding_frame = frame[h1:h2+1, w1:w2+1]
            bounding_thin_frame = thin_frame[h1:h2+1, w1:w2+1]
            bottom_line_list.append(bottom_line)
            cv.imwrite(f'{out_path}/frames/{start_ascii_code + i}.png', bounding_frame)
            cv.imwrite(f'{out_path}/thinning/{start_ascii_code + i}.png', bounding_thin_frame)
    return bottom_line_list

def pre_processing_on_img(imgs, start_ascii_code, out_path):
    img_bool, img_uint8, img_check = imgs
    count, label = object_counting(img_uint8)
    return extractFrames(img_check, label, count, img_bool, start_ascii_code, out_path)

def comfirm_thresholding(img, threshold):
    img_bool, img_uint8, img_check = thresholding(img, threshold)
    wind_name = 'check threshold '
    cv.namedWindow(wind_name)
    while(True):
        cv.imshow(wind_name, img_check)
        cv.waitKey(0)
        OK = input(f"fine thresholding? Enter a number to change threshold (current: {threshold}), or enter \"Y\" if you think its good.")
        try:
            threshold = int(OK)
            img_bool, img_uint8, img_check = thresholding(img, threshold)
        except:
            if OK == 'Y':
                break
            else:
                print('Please enter an integer or \"Y\".')
    cv.waitKey(1)
    cv.destroyAllWindows()
    cv.waitKey(1)
    return img_bool, img_uint8, img_check

def pre_processing(in_path, out_path, extension):    
    threshold = 90    
    frame_path = Path(f"{out_path}/frames")
    frame_path.mkdir(parents=True, exist_ok=True)
    frame_path = str(frame_path)
    thin_frame_path = Path(f"{out_path}/thinning")
    thin_frame_path.mkdir(parents=True, exist_ok=True)
    thresholded_imgs = []
    for i in range(1):
        print(f'start processing image {i}...')
        start_ascii_code = 33 + i * 6
        img_path = f"{in_path}/{i}{extension}"
        img = cv.imread(img_path, cv.IMREAD_GRAYSCALE)
        thresholded_imgs.append(comfirm_thresholding(img, threshold))
    bottom_line = []
    for i in range(1):
        bottom_line += pre_processing_on_img(thresholded_imgs[i], start_ascii_code, out_path)
    with open(in_path + "/bottom_line.txt", "w") as f:
        f.writelines("%s\n" % l for l in bottom_line)
    return frame_path
import numpy as np
import cv2 as cv
import MorphologicalProcessing as morpho
from pathlib import Path

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
    for i in range(1, count+1):
        I = np.where(label == i)
        if I[0].size < 30000:
            label[I] = 0
            error_count += 1
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
    print(count)
    for i in range(count):
        I = np.where(label == sort_ind[i] + 1)
        x_max, x_min, y_max, y_min = I[0].max(), I[0].min(), I[1].max(), I[1].min()
        frame = np.zeros((x_max-x_min+1, y_max-y_min+1), dtype=np.uint8)
        frame_bool = np.zeros((x_max-x_min+1, y_max-y_min+1), dtype=bool)
        I_frame = tuple([I[0] - x_min, I[1]-y_min])
        frame[I_frame] = img[I]
        frame_bool[I_frame] = img_bool[I]
        frame, frame_bool = cleanBoundary(frame, frame_bool)
        cv.imwrite(f'{out_path}/{start_ascii_code + i}.png', frame)
    return



# # read in image
# frame_path = sys.argv[1]
# raw_frame = cv.imread(frame_path, cv.IMREAD_GRAYSCALE)

# # find the frame
# MP = morpho.MorphologicalProcessing(raw_frame, t=85)
# # cv.imshow('check.png', MP.img_check)
# # cv.waitKey(0)
# # cv.destroyAllWindows()
# start_letter = 'A'
# count, label = MP.objectCounting()
# # cv.imshow('check.png', (label * (255 / label.max())).astype(np.uint8))
# # cv.waitKey(0)
# # cv.destroyAllWindows()
# extractFrames(MP.img_check, label, count, MP.img, ord(start_letter))

def pre_processing_on_img(img, threshold, start_ascii_code, out_path):
    MP = morpho.MorphologicalProcessing(img, t=threshold)
    count, label = MP.objectCounting()
    extractFrames(MP.img_check, label, count, MP.img, start_ascii_code, out_path)
    return 

def pre_processing(in_path, threshold, out_path, extension):        
    frame_path = Path(f"{out_path}/frames")
    frame_path.mkdir(parents=True, exist_ok=True)
    frame_path = str(frame_path)
    for i in range(16):
        start_ascii_code = 33 + i * 6
        img_path = f"{in_path}/{i}{extension}"
        img = cv.imread(img_path, cv.IMREAD_GRAYSCALE)
        pre_processing_on_img(img, threshold, start_ascii_code, frame_path)
    return frame_path

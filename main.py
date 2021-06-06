import sys
import numpy as np
import cv2
import MorphologicalProcessing as morpho
import Preprocessing as prepros
from modules import find_cut_point as fcp
import orientation as orien
import bounding_box as bb
from pathlib import Path
import devide_parts as dp
import transformation as tf
from modules import combine_parts as cp

def save_cut_points(img, i, cut_points):
    cut_p_dir = 'cut_points/'
    Path(cut_p_dir).mkdir(parents=True, exist_ok=True)
    # cut_points_img = np.zeros_like(img)
    cut_points_img = np.copy(img)
    # cut_points_img = np.full(cut_points_img.shape, 255)
    cut_points_img_name = cut_p_dir+str(i)+'.png'
    for point in cut_points:
        cut_points_img[tuple(point)] = 100
    cv2.imwrite(cut_points_img_name, cut_points_img.astype(np.uint8))

def save_parts(img, i, parts):
    part_dir = 'parts/'
    Path(part_dir).mkdir(parents=True, exist_ok=True)
    n = 0
    for part in parts:
        part_img_name = part_dir+str(i)+'_'+str(n)+'.png'
        part_img = np.zeros_like(img)
        part_img = np.full(part_img.shape, 255)
        for point in part:
            part_img[tuple(point)] = 0
        cv2.imwrite(part_img_name, part_img.astype(np.uint8))
        n += 1

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
        cv2.imwrite(part_img_name, part_img.astype(np.uint8))
        n += 1

def save_theta(img, i):
    orientation_dir = 'orientation_imgs/'
    Path(orientation_dir).mkdir(parents=True, exist_ok=True)
    file_name = orientation_dir + str(i) + '.png'
    img = (img - np.min(img)) / (np.max(img) - np.min(img)) * 255
    cv2.imwrite(file_name, img)

def save_combine_img(img, i):
    path_dir = 'combine_imgs/'
    Path(path_dir).mkdir(parents=True, exist_ok=True)
    file_name = path_dir + str(i) + '.png'
    cv2.imwrite(file_name, img)

# read in image
frame_path = sys.argv[1]
raw_frame = cv2.imread(frame_path, cv2.IMREAD_GRAYSCALE)

# find the frame
MP = morpho.MorphologicalProcessing(raw_frame, t=85)
start_letter = 'A'
count, label = MP.objectCounting()
prepros.extractFrames(MP.img_check, label, count, MP.img, ord(start_letter))

start_idx = ord('A')+1  # 
end_idx = ord('A')+1    # 
file_dir = 'frames'
file_dir = bb.get_bounding_box(file_dir, start_idx, end_idx)
cut_points_list = []


for i in range(start_idx, end_idx+1):
    img = cv2.imread(file_dir+str(i)+'.png', cv2.IMREAD_GRAYSCALE)
    theta = orien.get_orientation(img)
    save_theta(theta, i)
    cut_points, parts, connect_list = fcp.find_cut_point(img, theta)
    save_cut_points(img, i, cut_points)
    # print(len(parts))
    save_parts(img, i, parts)
    new_img, trans_parts, connect_list = tf.transform(img, parts, connect_list)
    save_trans_parts(new_img, i, trans_parts)
    combine_img = cp.combine_parts(new_img, trans_parts, connect_list)
    save_combine_img(combine_img, i)
# print(cut_points_list)

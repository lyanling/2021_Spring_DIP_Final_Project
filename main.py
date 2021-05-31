import sys
import numpy as np
import cv2
import MorphologicalProcessing as morpho
import Preprocessing as prepros
from modules import find_cut_point as fcp
import orientation as orien
import bounding_box as bb
from pathlib import Path


def save_cut_points(img, i, cut_points):
    cut_p_dir = 'cut_points/'
    Path(cut_p_dir).mkdir(parents=True, exist_ok=True)
    cut_points_img = np.zeros_like(img)
    cut_points_img = np.full(cut_points_img.shape, 255)
    cut_points_img_name = cut_p_dir+str(i)+'.png'
    for point in cut_points:
        cut_points_img[tuple(point)] = 0
    cv2.imwrite(cut_points_img_name, cut_points_img.astype(np.uint8))

def save_theta(img, i):
    orientation_dir = 'orientation_imgs/'
    Path(orientation_dir).mkdir(parents=True, exist_ok=True)
    file_name = orientation_dir + str(i) + '.png'
    img = (img - np.min(img)) / (np.max(img) - np.min(img)) * 255
    cv2.imwrite(file_name, img)


# read in image
frame_path = sys.argv[1]
raw_frame = cv2.imread(frame_path, cv2.IMREAD_GRAYSCALE)

# find the frame
MP = morpho.MorphologicalProcessing(raw_frame, t=85)
start_letter = 'A'
count, label = MP.objectCounting()
prepros.extractFrames(MP.img_check, label, count, MP.img, ord(start_letter))

start_idx = ord('A') # +1?
end_idx = ord('A') # +1?
file_dir = 'frames'
file_dir = bb.get_bounding_box(file_dir, start_idx, end_idx)
cut_points_list = []


for i in range(start_idx, end_idx+1):
    img = cv2.imread(file_dir+str(i)+'.png', cv2.IMREAD_GRAYSCALE)
    theta = orien.get_orientation(img)
    save_theta(theta, i)
    cut_points = fcp.find_cut_point(img, theta, threshold=150)
    cut_points_list.append(cut_points)
    save_cut_points(img, i, cut_points)
# print(cut_points_list)

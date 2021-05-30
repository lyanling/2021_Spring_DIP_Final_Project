import sys
import numpy as np
import cv2 as cv
import MorphologicalProcessing as morpho
import Pre-processing as prepros
from modules import find_cut_point as fcp
import orientation as orien
import bounding_box as bb

# read in image
frame_path = sys.argv[1]
raw_frame = cv.imread(frame_path, cv.IMREAD_GRAYSCALE)

# find the frame
MP = morpho.MorphologicalProcessing(raw_frame, t=85)
start_letter = 'A'
count, label = MP.objectCounting()
prepros.extractFrames(MP.img_check, label, count, MP.img, ord(start_letter))

start_idx = ord('A')
end_idx = ord('A')
file_dir = 'frame'
file_dir = bb.get_bounding_box(file_dir, start_idx, end_idx)
cut_points_list = []

for i in range(start_idx, end_idx+1):
    img = cv2.imread(file_dir+str(i)+'.png', cv2.IMREAD_GRAYSCALE)
    theta = orien.get_orientation(img)
    cut_points = fcp.find_cut_point(img, theta, threshold=60)
    cut_points_list.append(cut_points)
# print(cut_points_list)
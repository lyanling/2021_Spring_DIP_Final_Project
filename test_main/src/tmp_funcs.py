# for accesing and managing other functions
import pickle
from numpy.core.numeric import full
import orientation as orient
import cv2 as cv
from pathlib import Path
import numpy as np
import MorphologicalProcessing as morpho
from modules import find_cut_point as fcp
import classification as clf

def save_theta(img, i, out_path):
    orientation_dir = Path(f'{out_path}/orientation_imgs')
    orientation_dir.mkdir(parents=True, exist_ok=True)
    file_name = f'{orientation_dir}/{i}.png'
    img = (img - np.min(img)) / (np.max(img) - np.min(img)) * 255
    cv.imwrite(file_name, img)

def save_cut_points(img, i, cut_points, out_path):
    cut_p_dir = Path(f'{out_path}/cut_points/')
    cut_p_dir.mkdir(parents=True, exist_ok=True)
    cut_points_img = np.copy(img)
    cut_points_img_name = f'{cut_p_dir}/{i}.png'
    cut_points = np.array(cut_points).T
    if cut_points.size > 0:
        cut_points_img[tuple([cut_points[0], cut_points[1]])] = 100
    cv.imwrite(cut_points_img_name, cut_points_img.astype(np.uint8))

def save_parts(img, i, parts, out_path):
    part_dir = Path(f'{out_path}/parts')
    part_dir.mkdir(parents=True, exist_ok=True)
    part_img_name = f'{part_dir}/{i}.png'
    part_img = np.zeros_like(img)
    n = 1
    for part in parts:
        p = np.array(part).T
        part_img[tuple([p[0], p[1]])] = n
        n += 1
    save_img = part_img * (255 / part_img.max())
    cv.imwrite(part_img_name, save_img.astype(np.uint8))
    return part_img
    
def save_classify(img, i, label, out_path):
    class_dir = Path(f'{out_path}/classification')
    class_dir.mkdir(parents=True, exist_ok=True)
    full_label = clf.classify(img, label)
    save_img = full_label * (255 / full_label.max())
    save_img_path = f'{class_dir}/{i}.png'
    cv.imwrite(save_img_path, save_img.astype(np.uint8))
    return full_label

def get_frame_data(frame_path, thin_path, out_path):
    data_out_path = Path(f'{out_path}/data')
    data_out_path.mkdir(parents=True, exist_ok=True)
    for i in range(33, 33+6):
        print(f'start getting frame {i}\'s data')
        thin_img = cv.imread(f'{thin_path}/{i}.png', cv.IMREAD_GRAYSCALE)
        frame = cv.imread(f'{frame_path}/{i}.png', cv.IMREAD_GRAYSCALE)
        theta = orient.get_orientation(thin_img)
        save_theta(theta, i, out_path)
        cut_points, parts = fcp.find_cut_point(thin_img, theta)
        save_cut_points(thin_img, i, cut_points, out_path)
        label = save_parts(thin_img, i, parts, out_path)
        full_label = save_classify(frame, i, label, out_path)
        frame_data = full_label
        with open(f'{data_out_path}/{i}.pickle', 'wb') as fout:
            pickle.dump(frame_data, fout)
    return
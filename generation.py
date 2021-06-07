import numpy as np
import cv2 as cv
import combine_characters as cmbchar
import pickle
import transformation as tf
from modules import combine_parts as cp
from pathlib import Path

def load_infos(path):
    labels = []
    for i in range(33, 127):
        with open(f'{path}/data/{i}.pickle', 'rb') as fin:
            labels.append(pickle.load(fin))
    return labels

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
        cv.imwrite(part_img_name, part_img.astype(np.uint8))
        n += 1
    return 

def save_combine_img(img, i):
    path_dir = 'combine_imgs/'
    Path(path_dir).mkdir(parents=True, exist_ok=True)
    file_name = path_dir + str(i) + '.png'
    cv.imwrite(file_name, img)
    return 

def generate_word(input, paper, labels, connect_lists, fin_path):
    combined = None
    combined_floor = None
    for char in input:
        code = ord(char)
        label = labels[code-33]
        connect_list = connect_lists[code-33]
        img = cv.imread(f'{fin_path}/{code}.png', cv.IMREAD_GRAYSCALE)
        #transform
        new_img, trans_parts, connect_list = tf.transform(img, label, connect_list)
        save_trans_parts(new_img, i, trans_parts)
        #combine parts, out: combined_char
        combine_img = cp.combine_parts(new_img, trans_parts, connect_list)
        save_combine_img(combine_img, code)
        # new orientation and bounding box
        
        #combine char
        combined, combined_floor = cmbchar.combine_char(combined, )
        pass
    return

def generate_sentence(input, space, paper, labels, fin_path):
    words = input.split(' ')
    for word in words:
        generate_word(word, paper, labels, fin_path)
        # put space
    return

def generate_text(fin_path, space):
    paper = np.zeros((3508, 2480))
    labels = load_infos(fin_path)
    with open(fin_path, 'r') as fin:
        rows = fin.readlines()
        for row in rows:
            generate_sentence(row, space, paper, labels, fin_path)
            # new line
    return
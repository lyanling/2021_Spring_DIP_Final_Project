from abc import ABC
import numpy as np
import cv2 as cv
import transformation as tf
from modules import combine_parts as cp
import combine_characters as cmbchar
import pickle
from pathlib import Path
import gen_debug as debug
import bounding_box as box


def save_page(page_infos):
    path = page_infos['save path']
    page = page_infos['page']
    order = page_infos['order']
    text_name = page_infos['text name']
    cv.imwrite(f'{path}/{text_name}_{order}.png', page)
    return

def new_page(page_infos, size = (3508, 2480)):
    page_infos['page'] = np.zeros(size, dtype=np.uint8)
    page_infos['line offset'] = page_infos['header']
    page_infos['word offset'] = page_infos['word start']
    page_infos['order'] += 1
    return

def new_line(page_infos):
    page_infos['line offset'] += page_infos['leading']
    if page_infos['line_offset'] > page_infos['page'].shape[0] - page_infos['footer']:
        save_page(page_infos)
        new_page(page_infos)
    return

def load_infos(path, code):
    with open(f'{path}/data/{code}.pickle', 'rb') as fin:
        data = pickle.load(fin)
    # full_label, connect_list, avg_ori 
    return data

def generate_word(data_path, input, page_infos):
    combined = None
    combined_floor = None
    combined_ori = None
    for char in input:
        code = ord(char)
        label, connect_list, avg_ori  = load_infos(data_path, code)
        img = cv.imread(f'{data_path}/frames/{code}.png', cv.IMREAD_GRAYSCALE)
        #transform
        new_img, trans_parts, connect_list = tf.transform(img, label, connect_list, avg_ori)
        #combine parts, out: combined_char
        combine_img, combine_ori = cp.combine_parts(new_img, trans_parts, connect_list, avg_ori)
        # new orientation and bounding box
        bound, _ = box.get_bounding_box(combine_img)
        bottom_line = box.get_combined_bottom_line(combine_img, code, data_path)
        h1, h2, w1, w2 = bound
        bounded_combine_img = combine_img[h1:h2+1, w1:w2+1]
        combine_ori = combine_ori[h1:h2+1, w1:w2+1]
        #combine char (maybe it should tell us the orientation of left image)
        combined, combined_floor = cmbchar.combine_char(combined, bounded_combine_img, combined_ori, combine_ori, combined_floor, bottom_line, page_infos['tracking'])
    # paste the combined word to page
    if page_infos['word offset'] + combined.shape[1] > page_infos['word end']:
        new_line(page_infos)
    page = page_infos['page']
    paste_start = page_infos['line offset'] - combined_floor
    page[paste_start:paste_start + combined.shape[0], page_infos['word offset']:page_infos['word offset']+combined.shape[1]] = combined
    return

def generate_sentence(data_path, input, page_infos):
    words = input.split(' ')
    for word in words:
        generate_word(data_path, word, page_infos)
        # put space
        page_infos['word offset'] += page_infos['word-spacing']
        if page_infos['word offset'] > page_infos['page'].shape[1] - page_infos['word end']:
            new_line(page_infos)
    return

def generate_text(data_path, text_path, leading, word_spacing, tracking, header, footer):
    # init page
    size = (3508, 2480)
    page_infos = {}
    page_infos['save path'] = f'{data_path}/generate'
    page_infos['text name'] = Path(text_path).name
    page_infos['header'] = header
    page_infos['footer'] = footer
    page_infos['leading'] = leading
    page_infos['word-spacing'] = word_spacing
    page_infos['tracking'] = tracking
    page_infos['word start'] = 10
    page_infos['word end'] = 10
    page_infos['line offset'] = page_infos['header']
    page_infos['word offset'] = 10
    page_infos['order'] = 0
    page_infos['page'] = np.zeros(size, dtype=np.uint8)

    with open(text_path, 'r') as fin:
        rows = fin.readlines()
        for row in rows:
            generate_sentence(data_path, row, page_infos)
            # new line new page
            new_line(page_infos)
    save_page(page_infos)
    return
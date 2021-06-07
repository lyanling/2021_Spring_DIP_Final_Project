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

def load_infos(path):
    labels = []
    for i in range(33, 127):
        with open(f'{path}/data/{i}.pickle', 'rb') as fin:
            labels.append(pickle.load(fin))
    return labels

def generate_word(fin_path, input, tracking, page, labels, connect_lists, page_infos):
    combined = None
    combined_floor = None
    for char in input:
        code = ord(char)
        label = labels[code]
        connect_list = connect_lists[code-33]
        img = cv.imread(f'{fin_path}/{code}.png', cv.IMREAD_GRAYSCALE)
        #transform
        new_img, trans_parts, connect_list = tf.transform(img, label, connect_list)
        #combine parts, out: combined_char
        combine_img = cp.combine_parts(new_img, trans_parts, connect_list)
        # new orientation and bounding box
        bounded_combine_img, bottom_line = box.get_bounding_box(combine_img)

        #combine char (maybe it should tell us the orientation of left image)
        combined, combined_floor = cmbchar.combine_char(combined, bounded_combine_img, None, None, combined_floor, bottom_line, tracking)
    # paste the combined word to page
    if page_infos['word offset'] + combined.shape[1] > page['word end']:
        new_line(page_infos)
    page = page_infos['page']
    paste_start = page_infos['line offset'] - combined_floor
    page[paste_start:paste_start + combined.shape[0], page_infos['word offset']:page_infos['word offset']+combined.shape[1]] = combined
    return

def generate_sentence(fin_path, input, labels, page_infos):
    words = input.split(' ')
    for word in words:
        generate_word(fin_path, word, labels, page_infos)
        # put space
        page_infos['word offset'] += page_infos['word-spacing']
        if page_infos['word offset'] > page_infos['page'].shape[1] - page_infos['word end']:
            new_line(page_infos)
    return

def generate_text(fin_path, text_path, leading, word_spacing, tracking, header, footer):

    # init page
    size = (3508, 2480)
    page_infos = {}
    page_infos['save path'] = f'{fin_path}/generate'
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

    labels = load_infos(fin_path)
    with open(fin_path, 'r') as fin:
        rows = fin.readlines()
        for row in rows:
            generate_sentence(fin_path, row, labels, page_infos)
            # new line new page
            new_line(page_infos)
    save_page(page_infos)
    return
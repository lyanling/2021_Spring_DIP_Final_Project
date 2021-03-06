import numpy as np
import cv2 as cv
import transformation as tf
from modules import combine_parts as cp
import combine_characters as cmbchar
import pickle
import bounding_box as box
import resize
import changeColor as col
import webcolors

def save_page(page_infos):
    path = page_infos['save path']
    page = page_infos['page']
    page = col.changeColor(page, page_infos['font color'])
    page_infos['page'] = page
    if page_infos['bottom line']:
        draw_bottom_line(page_infos)
    order = page_infos['order']
    text_name = page_infos['text name']
    cv.imwrite(f'{path}/{text_name}_{order}.png', page)
    return

def new_page(page_infos, size = (3508, 2480)):
    page_infos['page'] = np.zeros(size, dtype=np.uint8)
    page_infos['page'].fill(255)
    page_infos['line offset'] = page_infos['header']
    page_infos['word offset'] = page_infos['word start']
    page_infos['order'] += 1
    return

def draw_bottom_line(page_infos):
    color = page_infos['bottom line color']
    color_rgb = webcolors.name_to_rgb(color)
    rgb = np.array([color_rgb[2], color_rgb[1], color_rgb[0]])
    page = page_infos['page']
    header = page_infos['header']
    leading = page_infos['leading']
    footer = page_infos['footer']
    for i in range(header, page.shape[0] - footer, leading):
        line = page[i, page_infos['word start']:-page_infos['word end']]
        draw_area = np.where(np.all(line == np.array([255, 255, 255]), axis=-1))
        line[draw_area, :] = rgb
        page[i, page_infos['word start']:-page_infos['word end']] = line
    page_infos['page'] = page
    return

def new_line(page_infos):
    page_infos['line offset'] += page_infos['leading']
    page_infos['word offset'] = page_infos['word start']
    if page_infos['line offset'] > page_infos['page'].shape[0] - page_infos['footer']:
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
    last_width = 0
    for char in input:
        code = ord(char)
        # print(code)
        # print(char)
        label, connect_list, avg_ori  = load_infos(data_path, code)
        img = cv.imread(f'{data_path}/frames/{code}.png', cv.IMREAD_GRAYSCALE)
        #transform
        parts = tf.label_to_parts(label)
        new_img, trans_parts, connect_list, avg_ori = tf.transform(img, parts, connect_list, avg_ori, code)
        #combine parts, out: combined_char
        combine_img, combine_ori = cp.combine_parts(new_img, trans_parts, connect_list, avg_ori)
        cv.imwrite(f'combined/{code}.png', combine_img)
        # closing
        combine_img = np.where(combine_img ==0, 255, 0).astype(np.uint8)
        combine_img  = cv.morphologyEx(combine_img , cv.MORPH_CLOSE, np.ones((5, 5)))
        combine_img = np.where(combine_img==0, 255, 0).astype(np.uint8)
        cv.imwrite(f'combined_closed/{code}.png', combine_img)
        # new orientation and bounding box
        bound, _ = box.get_bounding_box(combine_img)
        bottom_line = box.get_combined_bottom_line(combine_img, code, data_path)
        h1, h2, w1, w2 = bound
        combine_img = combine_img[h1:h2+1, w1:w2+1]
        combine_ori = combine_ori[h1:h2+1, w1:w2+1]
        # resize
        combine_img, bottom_line = resize.resize(combine_img, bottom_line, page_infos['font size'])
        combine_ori, _ = resize.resize(combine_ori, 0, page_infos['font size'])
        bound, _ = box.get_bounding_box(combine_img)
        h1, h2, w1, w2 = bound
        combine_img = combine_img[h1:h2+1, w1:w2+1]
        combine_ori = combine_ori[h1:h2+1, w1:w2+1]
        cv.imwrite(f'combined_resize/{code}.png', combine_img)
        #combine char (maybe it should tell us the orientation of left image)
        combined, combined_floor, combined_ori, last_width = cmbchar.combine_char(combined, combine_img, combined_ori, combine_ori, combined_floor, bottom_line, page_infos['tracking'], last_width)

    # paste the combined word to page
    if page_infos['word offset'] + combined.shape[1] > page_infos['page'].shape[1] - page_infos['word end']:
        new_line(page_infos)
    page = page_infos['page']
    # print(combined_floor)
    paste_start = page_infos['line offset'] - combined_floor
    # print(paste_start)
    paste_area = page[paste_start:paste_start + combined.shape[0], page_infos['word offset']:page_infos['word offset']+combined.shape[1]]
    paste_area = np.where(combined != 255, combined, paste_area)
    page[paste_start:paste_start + combined.shape[0], page_infos['word offset']:page_infos['word offset']+combined.shape[1]] = paste_area
    page_infos['page'] = page
    page_infos['word offset'] += combined.shape[1]
    return

def put_space(page_infos):
    page_infos['word offset'] += page_infos['word-spacing']
    if page_infos['word offset'] > page_infos['page'].shape[1] - page_infos['word end']:
        new_line(page_infos)
    return

def generate_sentence(data_path, input, page_infos):
    word = ''
    for char in input:
        if char == ' ':
            if word != '':
                generate_word(data_path, word, page_infos)
                word = ''
            # put space
            put_space(page_infos)
        elif char == '  ':
            if word != '':
                generate_word(data_path, word, page_infos)
                word = ''
            for i in range(4):
                put_space(page_infos)
        elif char == '\n':
            if word != '':
                generate_word(data_path, word, page_infos)
                word = ''
            new_line(page_infos)
        else:
            word += char
    if word != '':
        generate_word(data_path, word, page_infos)
        word = ''
    # words = input.split(' ')
    # for word in words:
    #     generate_word(data_path, word, page_infos)
    #     # put space
    #     page_infos['word offset'] += page_infos['word-spacing']
    #     if page_infos['word offset'] > page_infos['page'].shape[1] - page_infos['word end']:
    #         new_line(page_infos)
    return

def generate_text(data_path, text_path, page_infos):
    # init page
    size = (3508, 2480)
    page_infos['page'] = np.zeros(size, dtype=np.uint8)
    page_infos['page'].fill(255)
    with open(text_path, 'r') as fin:
        rows = fin.readlines()
        for row in rows:
            # row = row.strip()
            if len(row) > 0:
                generate_sentence(data_path, row, page_infos)
            else:
                # new line new page
                new_line(page_infos)
    save_page(page_infos)
    return
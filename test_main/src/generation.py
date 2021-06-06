import numpy as np
import cv2 as cv
import combine_characters as cmb
import transformation as trans
# combine parts
import combine_characters as cmbchar
import pickle

def load_infos():
    labels = []
    for i in range(33, 127):
        with open(f'./full_label/{i}.pickle', 'rb') as fin:
            labels.append(pickle.load(fin))
    return labels

def generate_word(input, paper, labels):
    combined = None
    combined_floor = None
    for char in input:
        code = ord(char)
        label = labels[code]
        #transform
        
        #combine parts, out: combined_char

        # new orientation and bounding box
        
        #combine char
        combined, combined_floor = cmbchar.combine_char(combined, )
        pass
    return

def generate_sentence(input, space, paper, labels):
    words = input.split(' ')
    for word in words:
        generate_word(word, paper, labels)
        # put space
    return

def generate_text(fin_path, space):
    paper = np.zeros(0)
    labels = load_infos()
    with open(fin_path, 'r') as fin:
        rows = fin.readlines()
        for row in rows:
            generate_sentence(row, space, paper, labels)
            # new line
    return
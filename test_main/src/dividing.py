import argparse
# import numpy as np
import pre_processing as pre
from pathlib import Path
# import cv2 as cv
import bounding_box as box
# import orientation as orient
import frame_data as fdata

parser = argparse.ArgumentParser(description='Part I: divide characters into parts : ) ) )', epilog="Run \"generating.py\" after this part!!")
parser.add_argument('in_path', help="input directory")
parser.add_argument('--out', dest="out_path", metavar="./MyHandWriting", default="./MyHandWriting",help="output directory")
parser.add_argument('--extension', dest="extension", metavar=".png", default=".jpg", help="extension of the input images")
args = parser.parse_args()


Path(args.out_path).mkdir(parents=True, exist_ok=True)
in_path = str(Path(args.in_path))
out_path = str(Path(args.out_path))


frame_path = f'{out_path}/frames'
thin_path = f'{out_path}/thinning'


# get frames
frame_path = pre.pre_processing(in_path, out_path, args.extension)

# thinning and bounding box 
thin_path = box.get_thinning_box(frame_path, out_path)

# save check image of orientation, cut points, and parts
# save frame data (cut points position, part labels)
fdata.get_frame_data(frame_path, thin_path, out_path)
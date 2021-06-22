import argparse
import pre_processing as pre
from pathlib import Path
import frame_data as fdata

parser = argparse.ArgumentParser(description='Part I: divide characters into parts : ) ) )', epilog="Run \"generating.py\" after this part!!")
parser.add_argument('in_path', help="input directory")
parser.add_argument('--out', dest="out_path", metavar="./MyHandWriting", default="./MyHandWriting" ,help="output directory")
parser.add_argument('--extension', dest="extension", metavar=".png", default=".jpg", help="extension of the input images")
args = parser.parse_args()


Path(args.out_path).mkdir(parents=True, exist_ok=True)
in_path = str(Path(args.in_path))
out_path = str(Path(args.out_path))


frame_path = f'{out_path}/frames'
thin_path = f'{out_path}/thinning'


# get frames and thinning
frame_path = pre.pre_processing(in_path, out_path, args.extension)

# save check image of orientation, cut points, and parts
# save frame data (cut points position, part labels)
fdata.get_frame_data(frame_path, thin_path, out_path)
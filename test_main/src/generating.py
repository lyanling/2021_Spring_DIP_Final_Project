import argparse
from pathlib import Path
import generation as gen

parser = argparse.ArgumentParser(description='Part II: generate your own handwritten script!!', epilog="Here you go : ) ) ) )")
parser.add_argument('in_path', help="input text file")
parser.add_argument('data_path', help="handwriting directory generate by \"dividing.py\"")

# parser.add_argument('--out', dest="out_path", metavar="./MyHandWriting", default="./MyHandWriting",help="output directory")
parser.add_argument('--l', dest="leading", types=int, default=0, help="leading")
parser.add_argument('--w', dest="word_spacing", types=int, default=0, help="word-spacing")
parser.add_argument('--t', dest="tracking", types=int, default=0, help="letter-spacing")

# letter size? color?

args = parser.parse_args()
gen_path = Path(f'{args.data_path}/generate')
gen_path.mkdir(parents=True, exist_ok=True)

gen.generate_text(str(gen_path), args.data_path ,args.leading, args.word_spacing, args.tracking, )
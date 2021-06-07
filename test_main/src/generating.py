import argparse
from pathlib import Path
import generation as gen

parser = argparse.ArgumentParser(description='Part II: generate your own handwritten script!!', epilog="Here you go : ) ) ) )")
parser.add_argument('text_path', help="input text file")
parser.add_argument('data_path', help="handwriting directory generate by \"dividing.py\"")

# parser.add_argument('--out', dest="out_path", metavar="./MyHandWriting", default="./MyHandWriting",help="output directory")
parser.add_argument('--l', dest="leading", type=int, default=300, help="leading")
parser.add_argument('--w', dest="word_spacing", type=int, default=50, help="word-spacing")
parser.add_argument('--t', dest="tracking", type=int, default=10, help="letter-spacing")
parser.add_argument('--header', dest="header", type=int, default=300, help="page header")
parser.add_argument('--footer', dest="footer", type=int, default=300, help="page footer")

# letter size? color?

args = parser.parse_args()
gen_path = Path(f'{args.data_path}/generate')
gen_path.mkdir(parents=True, exist_ok=True)
data_path = Path(args.data_path)
gen.generate_text(str(data_path), args.text_path ,args.leading, args.word_spacing, args.tracking, args.header, args.footer)
import argparse
from pathlib import Path
import generation as gen

parser = argparse.ArgumentParser(description='Part II: generate your own handwritten script!!', epilog="Here you go : ) ) ) )")
parser.add_argument('text_path', help="input text file")
parser.add_argument('data_path', help="handwriting directory generate by \"dividing.py\"")

# parser.add_argument('--out', dest="out_path", metavar="./MyHandWriting", default="./MyHandWriting",help="output directory")
parser.add_argument('--l', dest="leading", type=int, default=80, help="leading")
parser.add_argument('--w', dest="word_spacing", type=int, default=70, help="word-spacing")
parser.add_argument('--t', dest="tracking", type=int, default=5, help="letter-spacing")
parser.add_argument('--head', dest="header", type=int, default=300, help="page header")
parser.add_argument('--foot', dest="footer", type=int, default=300, help="page footer")
parser.add_argument('-b', dest="bottom_line", action='store_true',help="draw bottom line")
parser.add_argument('--s', dest="font_size", type=int, default=12, help="font size")

parser.add_argument('--bottom_line_color', dest="btlin_col", type=int, default=127, help="bottom line color")

# letter size? color?

args = parser.parse_args()
gen_path = Path(f'{args.data_path}/generate')
gen_path.mkdir(parents=True, exist_ok=True)
data_path = Path(args.data_path)

page_infos = {}
page_infos['save path'] = f'{data_path}/generate'
page_infos['text name'] = Path(args.text_path).name
page_infos['header'] = args.header
page_infos['footer'] = args.footer
page_infos['leading'] = args.leading
page_infos['word-spacing'] = args.word_spacing
page_infos['tracking'] = args.tracking
page_infos['word start'] = 10
page_infos['word end'] = 10
page_infos['line offset'] = page_infos['header']
page_infos['word offset'] = 10
page_infos['order'] = 0
page_infos['bottom line'] = args.bottom_line
page_infos['bottom line color'] = args.btlin_col
page_infos['font size'] = args.font_size

gen.generate_text(str(data_path), args.text_path ,page_infos)
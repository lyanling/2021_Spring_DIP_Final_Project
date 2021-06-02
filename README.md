# DIP_Final_Project
#### bounding_box.py :
`new_file_dir = get_bounding_box(file_dir, start_idx=33, end_idx=126)`:
  * input:
    * `file_dir` : directory name
    * `start_idx`, `end_idx` : ASCII code
  * output: 
    * `new_file_dir` : new directory name

`bottom_line = get_bottom_line(file_dir)`:
* `bottom_line`: list of bottom line locs of words
#### orientation.py :
`theta = get_orientation(img)`:
  * `img` : image of word
  * `theta` : orientation of word in array
#### transformation.py :
`new_cut_points_list, new_parts = transform(cut_points_list, parts)`:
  * input:
    * `cut_points_list` : list of cut points of a word : [[cp0x, cp0y], [cp1x, cp1y], ...]
    * `parts` : parts of a word in [set((x1, y1), (x2, y2), ...), set(), ...]
  * output: 
    * `new_cut_points_list` : 
      *  [[part1's connect_points_pairs], [], [], ...]
      *  part1's connect_points_pairs = [[X, part1's pointA, partX's point C], [Y, part1's point B, partY's point D], ...]
    * `new_parts` : same type as input

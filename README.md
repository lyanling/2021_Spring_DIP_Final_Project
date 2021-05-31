# DIP_Final_Project
#### bounding_box.py :
`get_bounding_box(file_dir, start_idx=33, end_idx=126)`:
  * input:
    * file_dir : directory name
    * start_idx, end_idx : ASCII code
  * output: new directory name

`get_bottom_line(file_dir)`:
* output: list of bottom line locs of words
#### orientation.py :
`get_orientation(img)`:
  * input : image of word
  * output : orientation of word in array
#### transformation.py :
`transform(cut_points_list, parts)`:
  * input:
    * cut_points_list : list of cut points of a word : [[cp0x, cp0y], [cp1x, cp1y], ...]
    * parts : parts of a word in [set((x1, y1), (x2, y2), ...), set(), ...]
  * output: 
    * new_cut_points_list : same type as input
    * new_parts : same type as input

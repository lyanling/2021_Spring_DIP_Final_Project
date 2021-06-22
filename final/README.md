# My Handwriting Generator

## Requirement
opencv-python 4.5.1
opencv-contrib-python 4.5.1
webcolors 1.11.1
## Usage
* Part I: divide characters into parts : ) ) )
    ```
    python3 pre_process.py [-h] [--out ./MyHandWriting] [--extension .png] in_path
    ```
    ```
    *********************************     hint     *******************************
    positional arguments:
  in_path               input directory
                        (containing the images of hanwritten words)

    optional arguments:
      -h, --help            show this help message and exit
      --out ./MyHandWriting
                        output directory
      --extension .png      extension of the input images

    Run "generating.py" after this part!!
    ******************************************************************************
    
    ```

* Part II: generate your own handwritten script!!
    ```
    generate.py [-h] [--l LEADING] [--w WORD_SPACING] [--t TRACKING] [--head HEADER] [--foot FOOTER] [-b] [--s FONT_SIZE] [--col FONT_COLOR]
                     [--btlin_col BTLIN_COL] [--initpos WORD_START] [--endpos WORD_END]
                     text_path data_path
    ```
    ```
    **********************************     hint     ************************************
    positional arguments:
      text_path             input text file
      data_path             handwriting directory generate by "dividing.py"

    optional arguments:
      -h, --help            show this help message and exit
      --l LEADING           leading, default: 80
      --w WORD_SPACING      word-spacing, default: 30
      --t TRACKING          letter-spacing, default: 5
      --head HEADER         page header, default: 150
      --foot FOOTER         page footer, default: 150
      -b                    draw bottom line
      --s FONT_SIZE         font size, default: 12
      --col FONT_COLOR      font color, default: black
      --btlin_col BTLIN_COL
                            bottom line color, default: gray
      --initpos WORD_START  word start position, default: 30
      --endpos WORD_END     word end position, default: 30

    Here you go : ) ) ) )
    ************************************************************************************
    ```
## Inputs
#### input image example
![](https://i.imgur.com/gC1Zn0D.jpg =400x)
![](https://i.imgur.com/myVTWH8.jpg =400x)
#### text.txt
```
I'm lazy in everything.
I don't wanna write anything.
My hands are not born for writing.
As a CSIE student.
Typing is everything.
Sorry for the bad rhyming.
Maybe you can do better than me.
```
## Result
![](https://i.imgur.com/860QGEs.png =500x)
![](https://i.imgur.com/1589Qvf.png =500x)
![](https://i.imgur.com/yyMKFFK.png =500x)
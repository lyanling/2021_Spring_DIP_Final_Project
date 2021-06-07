# DIP_Final_Project

* thinning.py - usage: \
  `import morphology.thinning as thin` \
  `thin_img = thin.thinning(img)`
  * convert to 8-bit unsigned int: \
    `thin_img = thin.thinning(img).astype(np.uint8)`
* find_cut_point.py - usage: \
  `from modules import find_cut_point as fcp` \
  `cut_points = fcp.find_cut_point(img, orientation, threshold=60)`
  * input: img, orientation`[-pi/2, pi/2]`, threshold(default: 60)
  * output: a list of cut points
    * cut_points = [p1, p2, ..., pn]
    * the form of each point: point = [x, y]

* test/
	* python3 main.py 2x4.png

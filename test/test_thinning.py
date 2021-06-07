import cv2
import numpy as np

img = cv2.imread("frames/66.png", cv2.IMREAD_GRAYSCALE)	# , cv2.IMREAD_GRAYSCALE
# img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
img_r = np.where(img == 0, 255, 0)
img_r = img_r.astype(np.uint8)
thinned = cv2.ximgproc.thinning(img_r) 	#
thinned = np.where(thinned == 0, 255, 0)
cv2.imwrite("66_thin.png", thinned)

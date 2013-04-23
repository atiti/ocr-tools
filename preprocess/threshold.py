#!/usr/bin/env python

import cv, cv2, sys
im_gray = cv2.imread(sys.argv[1], cv.CV_LOAD_IMAGE_GRAYSCALE)
(thres, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
cv2.imwrite('test.png', im_bw)

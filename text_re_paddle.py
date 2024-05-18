from method.utils import *
import cv2
from paddleocr import PaddleOCR

import logging

__author__ = "user"
logger = logging.getLogger("ppocr")
logger.setLevel(logging.ERROR)

x = get_png_files("x/")

ocr = PaddleOCR(use_angle_cls=True)

for png in x:
    screen = cv2.imread("x/" + png)
    cropped_image = screen[44:64, 15:150]

    result = ocr.ocr(cropped_image)[0]
    print(result)
    '''
    _ = []
    for r in result:
        _.append(r[1][0])
    stri = "".join(_)
    print(stri)'''

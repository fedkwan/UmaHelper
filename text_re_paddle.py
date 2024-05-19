from method.utils import *
from module.cultivate.get_round import *
from method.recognition.textRecognizer import *
import cv2
from paddleocr import PaddleOCR
# import ddddocr

import logging
import onnxruntime as ort

__author__ = "user"
logger = logging.getLogger("ppocr")
logger.setLevel(logging.ERROR)

x = get_png_files("x/")

ocr = PaddleOCR(use_angle_cls=True)
import easyocr

ort.set_default_logger_severity(3)
# ocr = ddddocr.DdddOcr()

for png in x:
    screen = cv2.imread("x/" + png)
    print(png)
    cropped_image = screen[44:64, 15:150]

    # reader = easyocr.Reader(['ch_tra'])
    # result = reader.readtext(cropped_image)

    result = ocr.ocr(cropped_image)[0]
    print(result)
    '''
    _ = []
    for r in result:
        _.append(r[1][0])
    stri = "".join(_)
    print(stri)
    try:
        this_round = get_round(screen, ocr)
        print(this_round)
        print("==========")
    except Exception as e:
        print(e)
        continue
    '''

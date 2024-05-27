import numpy as np
from method.image_handler import *


def get_attribute(ocr: ddddocr.DdddOcr, screen: np.array):
    # attribute
    x_li = [72, 185, 297, 410, 522]
    attribute_li = []
    for x in x_li:
        cropped_image = screen[855:882, x:x + 66]
        handler = ImageHandler()
        number = handler.get_text_from_image_dddd(ocr, cropped_image)
        try:
            attribute_li.append(int(number))
        except ValueError as e:
            print(e)
            attribute_li.append(0)  # 这里可能会存在数字无法转换的情况，概率很小，可以忽略
    return attribute_li

# get_pt [854:905, 599:695]

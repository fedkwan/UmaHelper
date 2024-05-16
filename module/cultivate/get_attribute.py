import numpy
from method.recognition.textRecognizer import *
import ddddocr

"""
    获取马娘的五维数值，返回一个数组，目前在 Ura 和 青春杯都适用。
"""


def get_attribute(screen: numpy.ndarray, ocr: ddddocr.DdddOcr()):
    # 获取当前五维
    x_li = [72, 185, 297, 410, 522]
    result_li = []
    for x in x_li:
        cropped_image = screen[855:882, x:x + 66]
        text_recognizer = TextRecognizer(cropped_image, ocr)
        number = text_recognizer.find_text_from_image()  # 这里可能会存在数字无法转换的情况，概率很小，可以忽略
        try:
            result_li.append(int(number))
        except ValueError as e:
            print(e)
            result_li.append(0)
    return result_li


# test
if __name__ == "__main__":
    # _d = u2.connect("127.0.0.1:16384")
    # _screen = _d.screenshot(format="opencv")
    import cv2
    import uiautomator2 as u2
    _screen = cv2.imread("../../temp.png")
    _ocr = ddddocr.DdddOcr()
    print(get_attribute(_screen, _ocr))
    print(type(_screen))

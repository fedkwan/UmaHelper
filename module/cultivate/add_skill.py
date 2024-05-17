import cv2
import uiautomator2 as u2
import numpy as np
from method.recognition.textRecognizer import *
from paddleocr import PaddleOCR
import logging

__author__ = "user"
logger = logging.getLogger("ppocr")
logger.setLevel(logging.ERROR)


def add_skill(d: u2.connect(), ocr: PaddleOCR()):
    screen = d.screenshot(format="opencv")


def fix_swipe(d: u2.connect()):
    screen = d.screenshot(format="opencv")
    i = 0
    for i in range(472, 1280):
        if np.all(screen[i, 360] != np.array([255, 255, 255])):
            break
    print(i)
    gap = i - 472
    d.swipe(360, 900, 360, 900 - gap * 1.8)


def get_box_boundary(screen: np.ndarray):
    # 获取当前屏幕内技能方框的纵坐标组
    y_li = []
    y = 472  # 472 到 1028 是技能列表的范围
    while y < 1028:
        if np.all(screen[y, 360] == np.array([210, 193, 193])):
            y_li.append(y)
        y += 1
    print(y_li)

    # 将相邻且差值为1的两个数取小数
    adjust_li = []
    i = 0
    while i < len(y_li):
        if y_li[i + 1] - y_li[i] == 1:
            adjust_li.append(y_li[i])
            i += 2  # 跳过这对数字
        else:
            adjust_li.append(y_li[i])
            i += 1
    print(adjust_li)

    # 计算出坐标对
    '''
    5个数：1上，2下，3上，4下，5上
    6个数：1下，2上，3下，4上，5下，6上
    7个数：1上，2下，3上，4下，5上，6下，7上
    8个数：1下，2上，3下，4上，5下，6上，7下，8上
    '''
    result = []
    for i in range(1, len(adjust_li)):
        if adjust_li[i] - adjust_li[i - 1] > 100:
            result.append([adjust_li[i - 1], adjust_li[i]])
            i += 1  # 跳过这对数字
    return result


# test
if __name__ == "__main__":
    _d = u2.connect("127.0.0.1:16384")
    _ocr = PaddleOCR()
    _screen = _d.screenshot(format="opencv")
    gg = get_box_boundary(_screen)
    print(gg)

    text_li = []
    for g in gg:
        cropped_image = _screen[g[0]:g[0] + 52, 138:482]
        _result = _ocr.ocr(cropped_image)[0][0][1][0]
        text_li.append(_result)
    print(text_li)

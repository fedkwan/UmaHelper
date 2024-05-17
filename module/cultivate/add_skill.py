import time

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
    all_skill_text_li = []
    count = 0
    while True:
        screen = d.screenshot(format="opencv")

        boundary_li = get_box_boundary(screen)
        for g in boundary_li:
            cropped_image = screen[g[0]:g[0] + 52, 138:482]
            _result = _ocr.ocr(cropped_image)[0][0][1][0]
            all_skill_text_li.append(_result)

        d.swipe(360, 900, 360, 500, 1)

        if count == 1:
            break

        if np.all(screen[1013, 700] == np.array([142, 120, 125])):
            count += 1

        time.sleep(1)

    return all_skill_text_li


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
    while i < len(y_li) - 1:
        if y_li[i + 1] - y_li[i] == 1:
            adjust_li.append(y_li[i])
            i += 2  # 跳过这对数字
        else:
            adjust_li.append(y_li[i])
            i += 1
    if i == len(y_li) - 1:
        adjust_li.append(y_li[i])
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

    l = add_skill(_d, _ocr)

    print(l)



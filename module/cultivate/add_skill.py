import time

import cv2
import uiautomator2 as u2
import numpy as np
import logging
from paddleocr import PaddleOCR

from method.recognition.textRecognizer import *
from method.textSimilarity import *
from module.cultivate.skill_dic import *

__author__ = "user"
logger = logging.getLogger("ppocr")
logger.setLevel(logging.ERROR)


def add_skill(d: u2.connect(), ocr: PaddleOCR(), to_add_skill_list: []):
    all_skill_text_li = []
    count = 0
    while True:
        screen = d.screenshot(format="opencv")

        boundary_li = get_box_boundary(screen)
        for g in boundary_li:
            cropped_image = screen[g[0]:g[0] + 155, 138:483]
            result = ocr.ocr(cropped_image)[0]
            _ = []
            for r in result:
                _.append(r[1][0])
            ocred_skill_text = "".join(_)

            most_similar_string = find_most_similar_string(ocred_skill_text, skill_dic_combine_name_and_description)

            skill_text = skill_dic_combine_name_and_description_reversal[most_similar_string]
            print(skill_text)

            if skill_text in to_add_skill_list:
                d.click(650, g[0] + 75)
                time.sleep(1)
                continue

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
        # 灰色或者金色边界，如果改了UI就要重新适配颜色咯
        if np.all(screen[y, 360] == np.array([210, 193, 193])) or np.all(screen[y, 360] == np.array([57, 193, 255])):
            y_li.append(y)
        y += 1
    # print(y_li)

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
    # print(adjust_li)

    # 计算出坐标对
    '''
    5个数：1上，2下，3上，4下，5上 / 1下，2上，3下，4上，5下
    6个数：1下，2上，3下，4上，5下，6上
    7个数：1上，2下，3上，4下，5上，6下，7上 / 1下，2上，3下，4上，5下，6上，7下
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

    _to_add = ["貪吃鬼"]
    ll = add_skill(_d, _ocr, _to_add)
    print(ll)
    # x = get_box_boundary(_screen)
    # print(x)

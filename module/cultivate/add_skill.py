import time
import importlib

import uiautomator2 as u2
from paddleocr import PaddleOCR

from setting.base import *
from method.utils import *
from method.text_handler import *
from method.image_handler import *
from module.cultivate.skill_dic import *


def add_skill(d, ocr):

    screen = d.screenshot(format="opencv")
    _image = screen[406:436, 530:630]
    handler = ImageHandler()
    text = handler.get_text_from_image(ocr, _image)
    num = find_numbers_in_string(text, "rude")
    if num < 100:
        d.click(80, 1180)
        time.sleep(DEFAULT_SLEEP_TIME)

    print("准备开始第1轮")
    # 第一轮，加列表内的技能
    add_skill_run(d, 1)
    scroll_to_top()

    print("准备开始第2轮")

    # 第二轮，加跑法和距离技能
    add_skill_run(d, 2)
    scroll_to_top()

    print("准备开始第3轮")

    # 第三轮，加完技能点
    add_skill_run(d, 3)

    screen = d.screenshot(format="opencv")
    _image = screen[406:436, 530:630]
    handler = ImageHandler()
    text = handler.get_text_from_image(ocr, _image)
    num = find_numbers_in_string(text, "rude")
    print(num)
    if num < 100:
        d.click(80, 1080)

def add_skill_run(d, step, ocr, p_ocr, setting_dic):

    while True:

        screen = d.screenshot(format="opencv")
        _image = screen[406:436, 530:630]
        handler = ImageHandler()
        text = handler.get_text_from_image(ocr, _image)
        num = find_numbers_in_string(text, "rude")
        print(num)
        if num < 100:
            d.click(360, 1080)
            break

        boundary_li = get_box_boundary(screen)
        for g in boundary_li:
            cropped_image = screen[g[0] : g[0] + 155, 138:483]

            # 识别技能名
            result = p_ocr.ocr(cropped_image)[0]
            ocred_skill_text = "".join(r[1][0] for r in result)
            handler = TextHandler()
            most_similar_string = handler.find_most_similar_str(
                ocred_skill_text, skill_dic_combine_name_and_description
            )
            skill_text = skill_dic_combine_name_and_description_reversal[
                most_similar_string
            ]
            print(skill_text)

            if step == 1:
                if skill_text in setting_dic["add_skill_list"]:
                    d.click(650, g[0] + 75)
                    continue
            if step == 2:
                if (
                    setting_dic["add_skill_running_style"] in skill_text
                    or setting_dic["add_skill_running_distance"] in skill_text
                ):
                    d.click(650, g[0] + 75)
                    continue
            if step == 3:
                d.click(650, g[0] + 75)

        d.swipe(360, 900, 360, 500, 1)

        if np.all(screen[1013, 700] == np.array([142, 120, 125])):
            print("xxx")
            break
        time.sleep(DEFAULT_SLEEP_TIME)

def scroll_to_top(d):
    while True:
        screen = d.screenshot(format="opencv")
        if np.all(screen[480, 700] == np.array([142, 120, 125])):
            break
        d.swipe(360, 500, 360, 1200, 0.2)
        time.sleep(0.2)

@staticmethod
def get_box_boundary(screen: np.ndarray):
    # 获取当前屏幕内技能方框的纵坐标组
    y_li = []
    y = 472  # 472 到 1028 是技能列表的范围
    while y < 1028:
        # 灰色或者金色边界，如果改了UI就要重新适配颜色
        if np.all(screen[y, 360] == np.array([210, 193, 193])) or np.all(
            screen[y, 360] == np.array([57, 193, 255])
        ):
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
    """
    5个数：1上，2下，3上，4下，5上 / 1下，2上，3下，4上，5下
    6个数：1下，2上，3下，4上，5下，6上
    7个数：1上，2下，3上，4下，5上，6下，7上 / 1下，2上，3下，4上，5下，6上，7下
    8个数：1下，2上，3下，4上，5下，6上，7下，8上
    """
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
    _setting_dic = importlib.import_module("customer_setting.setting_1").data

import re

import uiautomator2 as u2
import numpy as np

from method.base import *
from method.image_handler import *

logging.getLogger("airtest").setLevel(logging.ERROR)


def get_round(screen: np.array, ocr: PaddleOCR) -> int:
    # round
    cropped_image = screen[44:64, 15:150]
    handler = ImageHandler()
    round_text = handler.get_text_from_image_paddle(ocr, cropped_image)
    round_num = round_text_to_round_num(round_text)
    return round_num


def round_text_to_round_num(round_text: str) -> int:
    round_text = round_text.replace(" ", "")  # 去除空格
    print(round_text)
    round_num, year, month, half = 99, 99, 99, 99
    if "新" in round_text or "手" in round_text:
        year = 0
        if "出" in round_text:
            return 1
        else:
            month = find_numbers_in_string(round_text) - 1
            half = 0 if "前" in round_text else 1
    elif "典" in round_text:
        year = 1
        month = find_numbers_in_string(round_text) - 1
        half = 0 if "前" in round_text else 1
    elif "深" in round_text:
        year = 2
        month = find_numbers_in_string(round_text) - 1
        half = 0 if "前" in round_text else 1
    elif "系" in round_text:
        return 1
    if month > 11:
        return 2674
    round_num = (
        2 * (12 * year + month) + half + 1
    )  # 如果都是99，说明识别出问题了，这里会是 2674
    return round_num


def competition_round_text_to_round_num(d: u2.connect, ocr: PaddleOCR) -> int:
    print("看不清楚回合数！")
    while True:
        screen = d.screenshot(format="opencv")

        if np.all(screen[853, 120] == screen[906, 350]) and np.all(
            screen[853, 350] == screen[906, 580]
        ):
            # 根据技能按钮底部的粉蓝色判断是不是培育主界面
            if np.all(screen[1020, 550] == np.array([215, 195, 43])):
                d.click(510, 1130)
                time.sleep(DEFAULT_SLEEP_TIME)

        # 显示粉丝的小人头
        if np.all(screen[580, 36] == np.array([134, 126, 255])) and np.all(
            screen[560, 36] == np.array([134, 126, 255])
        ):
            cropped_image = screen[625:675, 220:500]
            handler = ImageHandler()
            round_text = handler.get_text_from_image_paddle(ocr, cropped_image)
            print(round_text)
            round_num = round_text_to_round_num(round_text)
            d.click(90, 1230)
            time.sleep(DEFAULT_SLEEP_TIME * 6)
            if round_num == 2674:
                round_num = 0
            return round_num


def find_numbers_in_string(string, model="stable"):
    numbers = re.findall(r"\d+", string)
    if not numbers:
        if model == "stable":
            return None
        elif model == "rude":
            return 0
    return int("".join(numbers))


# test
if __name__ == "__main__":
    _d = u2.connect("127.0.0.1:16384")
    _screen = _d.screenshot(format="opencv")
    _ocr = PaddleOCR(use_angle_cls=True)
    print(get_round(_screen, _ocr))

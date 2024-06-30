import importlib

import uiautomator2 as u2

from setting.base import *
from method.image_handler import *


def chose_uma(d: u2.connect, p_ocr: PaddleOCR, setting_dic: dict):

    uma_name = setting_dic["uma_name"]
    uma_chinese_name = setting_dic["uma_chinese_name"]

    screen = d.screenshot(format="opencv")
    text_image = screen[415:445, 35:155]
    handler = ImageHandler()
    text = handler.get_text_from_image_paddle(p_ocr, text_image)
    print(uma_name)
    print(text)
    if text == uma_chinese_name:
        return

    icon_dir = ROOT_DIR + "/resource/icon"
    sub_image = cv2.imread(icon_dir + "/" + uma_name + ".png")

    scroll_to_top(d)

    while True:
        screen = d.screenshot(format="opencv")
        handler = ImageHandler()
        best_match = handler.find_sub_image(sub_image, screen, 0.7)
        if best_match is not None:
            click_x, click_y = best_match["result"]
            d.click(click_x, click_y)
            break
        else:
            d.swipe(360, 900, 360, 700, 1)
            time.sleep(DEFAULT_SLEEP_TIME)


def scroll_to_top(d: u2.connect):
    while True:
        screen = d.screenshot(format="opencv")
        if np.all(screen[655, 695] == np.array([142, 120, 125])):
            break
        d.swipe(360, 700, 360, 1200, 0.5)
        time.sleep(DEFAULT_SLEEP_TIME)


# test
if __name__ == "__main__":
    _d = u2.connect("127.0.0.1:16384")
    _p_ocr = PaddleOCR()
    _setting_dic = importlib.import_module("customer_setting.setting_2").data
    chose_uma(_d, _p_ocr, _setting_dic)

import importlib

import uiautomator2 as u2

from method.base import *
from method.utils import *
from method.image_handler import *


def chose_uma(d: u2.connect, setting_dic: dict):

    uma_name = setting_dic["uma_name"]
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
    _setting_dic = importlib.import_module("customer_setting.setting_1").data
    chose_uma(_d, _setting_dic)

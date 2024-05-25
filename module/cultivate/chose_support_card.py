import uiautomator2 as u2
import importlib
import time
import numpy as np
import cv2
from method.utils import *
from method.recognition.imageMatcher import *


def chose_support_card(d: u2.connect(), setting_file_name):
    setting_data = importlib.import_module("customer_setting" + "." + setting_file_name).data

    support_card_name = setting_data["support_card_png_name"]
    png_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/resource/support_card/" + support_card_name
    prat_image = cv2.imread(png_path)

    while True:
        screen = d.screenshot(format="opencv")

        if np.all(screen[240, 480] == np.array([73, 201, 73])):
            if np.all(screen[679, 571] == np.array([23, 219, 153])):
                d.click(571, 679)
                time.sleep(DEFAULT_SLEEP_TIME)
            else:
                d.click(360, 1080)
                time.sleep(DEFAULT_SLEEP_TIME * 2)

        if np.all(screen[40, 360] == np.array([8, 215, 146])) and np.all(screen[85, 360] == np.array([12, 195, 109])):
            # 如果不是确认页面
            if np.all(screen[1060, 60] != np.array([73, 201, 73])):
                image_matcher = ImageMatcher(prat_image, screen, 0.7)
                best_match = image_matcher.find_part_image_from_total_image()
                if best_match is not None:
                    x, y = best_match["result"]
                    d.click(x, y)
                    time.sleep(DEFAULT_SLEEP_TIME)
                else:
                    d.swipe(360, 900, 360, 300)
                    time.sleep(DEFAULT_SLEEP_TIME)
            else:
                d.click(530, 1180)
                break


def scroll_to_top(d: u2.connect()):
    while True:
        screen = d.screenshot(format="opencv")
        if np.all(screen[655, 695] == np.array([142, 120, 125])):
            break
        d.swipe(360, 700, 360, 1200, 0.5)
        time.sleep(DEFAULT_SLEEP_TIME)


# test
if __name__ == "__main__":
    _d = u2.connect("127.0.0.1:16384")
    chose_support_card(_d, "setting_1")

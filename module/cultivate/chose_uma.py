import uiautomator2 as u2
import importlib
import time
import numpy as np
from method.utils import *
from method.recognition.imageMatcher import *


def chose_uma(d: u2.connect(), setting_file_name):
    setting_data = importlib.import_module("customer_setting" + "." + setting_file_name).data

    uma_name = setting_data["uma_name"]
    icon_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/resource/uma_file/icon"
    prat_image = cv2.imread(icon_dir + "/" + uma_name + ".png")

    scroll_to_top(d)

    while True:
        screen = d.screenshot(format="opencv")
        image_matcher = ImageMatcher(prat_image, screen)
        best_match = image_matcher.find_part_image_from_total_image()

        if best_match is not None:
            x, y = best_match["result"]
            d.click(x, y)
            time.sleep(DEFAULT_SLEEP_TIME)
            d.click(360, 1080)
            break

        else:
            d.swipe(360, 900, 360, 700, 1)
        time.sleep(DEFAULT_SLEEP_TIME)


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
    chose_uma(_d, "setting_1")

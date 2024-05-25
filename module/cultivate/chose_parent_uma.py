import uiautomator2 as u2
import importlib
import time
import numpy as np
import cv2
from method.utils import *
from method.recognition.imageMatcher import *


def enter_chose_parent_uma(d: u2.connect(), setting_file_name):
    setting_data = importlib.import_module("customer_setting" + "." + setting_file_name).data

    uma_rank_1 = setting_data["parent_uma_rank_1"]
    uma_rank_2 = setting_data["parent_uma_rank_2"]
    uma_rank_friend = setting_data["parent_uma_rank_friend"]

    # 如果没有遗传树
    while True:
        screen = d.screenshot(format="opencv")

        if np.all(screen[660, 110] == np.array([247, 179, 36])):
            if np.all(screen[775, 215] != np.array([196, 196, 196])):
                d.click(110, 800)
                time.sleep(DEFAULT_SLEEP_TIME)
            elif np.all(screen[775, 555] != np.array([196, 196, 196])):
                d.click(450, 800)
                time.sleep(DEFAULT_SLEEP_TIME)

        if np.all(screen[690, 360] == np.array([245, 194, 87])):
            chose_parent_uma(d, uma_rank_1)

        if np.all(screen[690, 360] == np.array([193, 142, 251])):
            if np.all(screen[635, 700] == np.array([117, 50, 255])):
                d.click(530, 655)
                time.sleep(DEFAULT_SLEEP_TIME)
                chose_parent_uma(d, uma_rank_friend)
            else:
                chose_parent_uma(d, uma_rank_2)

        time.sleep(DEFAULT_SLEEP_TIME)

        png_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/resource/general/ok.png"
        prat_image = cv2.imread(png_path)
        image_matcher = ImageMatcher(prat_image, screen)
        best_match = image_matcher.find_part_image_from_total_image()
        if best_match is not None:
            x, y = best_match["result"]
            d.click(x, y)
            time.sleep(DEFAULT_SLEEP_TIME)

        if np.all(screen[775, 215] == np.array([196, 196, 196])) and np.all(screen[775, 555] == np.array([196, 196, 196])):
            d.click(360, 1080)
            time.sleep(DEFAULT_SLEEP_TIME)
            break


def chose_parent_uma(d: u2.connect(), rank):
    rank = rank - 1
    count = 0
    while True:
        screen = d.screenshot(format="opencv")
        li = []
        for y in range(691, 972):
            rgb_sum = np.sum(screen[y, 427])
            if rgb_sum < 720:
                li.append(y)

        merged_array = merge_close_values(li)

        x_li = [90, 225, 360, 495, 630, 90, 225, 360, 495, 630]
        if int(rank / 10) == count:
            p = rank % 10
            if p <= 5:
                d.click(x_li[p], merged_array[0])
                time.sleep(DEFAULT_SLEEP_TIME)
                d.click(360, 1080)
            elif p > 5:
                d.click(x_li[p], merged_array[1])
                time.sleep(DEFAULT_SLEEP_TIME)

                # 决定
                d.click(360, 1080)
            break

        d.swipe(360, 900, 360, 600, 1)
        count = count + 1
        time.sleep(DEFAULT_SLEEP_TIME)


# test
if __name__ == "__main__":
    _d = u2.connect("127.0.0.1:16384")
    enter_chose_parent_uma(_d, "setting_1")

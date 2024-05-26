import time
import datetime
import importlib

import uiautomator2 as u2
import cv2
from paddleocr import PaddleOCR
import numpy as np

from method.base import *
from method.utils import *
from method.image_handler import *


class Competition:
    def __init__(self, d: u2.connect(), ocr: PaddleOCR(), setting_file="setting_1"):
        self.dir = ROOT_DIR + "/resource/competition"
        self.d = d
        self.ocr = ocr
        setting_data = importlib.import_module("customer_setting" + "." + setting_file)
        self.setting_dic = setting_data.data

    def competition(self):

        # 进入竞赛首页
        while True:
            screen = self.d.screenshot(format="opencv")

            # 如果是【游戏登录后】的首页
            # 定位底栏【主页面】蓝色
            if np.all(screen[1261, 360] == np.array([247, 159, 28])):
                self.d.click(520, 1220)
                time.sleep(DEFAULT_SLEEP_TIME)
                continue

            # 如果是【竞赛】的首页
            gray = np.array([109, 84, 89])
            # 用4个方块的底部的灰线上的点的颜色来定位当前页面
            if np.all(screen[950, 320] == gray) and np.all(screen[950, 400] == gray) and np.all(screen[1106, 320] == gray) and np.all(
                    screen[1106, 400] == gray):

                # 判断是不是每周结算时刻
                current_time = datetime.datetime.now()
                is_weekend_midnight = (current_time.weekday() == 0 and current_time.hour < 5)

                # 判断第一格RP点槽是否为灰色，如果不是，说明还有RP点
                # 如果有RP点，也不是结算时刻，那就先进行队伍竞技场
                if np.all(screen[65, 430] != np.array([89, 76, 81])) and is_weekend_midnight is False:
                    self.d.click(200, 850)
                    time.sleep(DEFAULT_SLEEP_TIME)
                    continue
                # 否则前往每日挑战内容
                else:
                    self.d.click(200, 1050)
                    time.sleep(DEFAULT_SLEEP_TIME)
                    continue

            # 如果是【队伍竞技场】的首页
            weekend_gray = np.array([70, 52, 57])
            # 用2个方块的底部的灰线上的点的颜色来定位当前页面
            # 判断是不是每周结算时刻，是的话返回
            if np.all(screen[875, 360] == weekend_gray) and np.all(screen[1015, 360] == gray):
                self.d.click(80, 1080)
                time.sleep(DEFAULT_SLEEP_TIME)
                continue
            if np.all(screen[875, 360] == gray) and np.all(screen[1015, 360] == gray):
                # 判断第一格RP点槽是否为灰色，如果不是，说明还有RP点（跟上面重复的，再一次判定）
                if np.all(screen[65, 430] != np.array([89, 76, 81])):
                    self.d.click(360, 820)
                    time.sleep(DEFAULT_SLEEP_TIME)
                    continue
                else:
                    self.d.click(80, 1080)
                    time.sleep(DEFAULT_SLEEP_TIME)
                    continue

            # 如果是【队伍竞赛】挑选对手的页面
            # 用3个方块的底部的灰线上的点的颜色来定位当前页面
            opponent_gray = np.array([123, 91, 97])
            if np.all(screen[476, 360] == opponent_gray) and np.all(screen[746, 360] == opponent_gray) and np.all(
                    screen[1016, 360] == opponent_gray):
                # 默认选第3个对手
                self.d.click(360, 900)
                time.sleep(DEFAULT_SLEEP_TIME * 2)
                continue

            # 如果是【每日竞赛内容】的首页
            # 用2个方块的底部的灰线上的点的颜色来定位当前页面
            if np.all(screen[1030, 320] == gray) and np.all(screen[1030, 400] == gray):
                # 先看左边还有没有次数
                cropped_image = screen[949:973, 120:300]
                handler = ImageHandler()
                daily_competition_status_text = handler.get_text_from_image(self.ocr, cropped_image)
                if "束" not in daily_competition_status_text:
                    self.d.click(210, 930)
                    time.sleep(DEFAULT_SLEEP_TIME)
                    continue

                # 再看右边有没有次数
                cropped_image = screen[949:973, 420:600]
                handler = ImageHandler()
                daily_legend_competition_status_text = handler.get_text_from_image(self.ocr, cropped_image)
                if "束" not in daily_legend_competition_status_text:
                    self.d.click(510, 930)
                    time.sleep(DEFAULT_SLEEP_TIME)
                    continue

                # 如果都没次数，就退出循环了（后续如果要打传奇赛的话这里要改掉）
                if "束" in daily_competition_status_text and "束" in daily_legend_competition_status_text:
                    self.d.click(360, 1220)  # 回到首页
                    print("竞赛结束")
                    time.sleep(DEFAULT_SLEEP_TIME)
                    break

            # 如果是【每日竞赛】，选择月光赏或者木星杯的页面
            if np.all(screen[640, 33] == np.array([138, 115, 100])) and np.all(screen[783, 33] == np.array([128, 105, 90])):
                cropped_image = screen[11:37, 610:690]
                handler = ImageHandler()
                daily_competition_left_times_text = handler.get_text_from_image(self.ocr, cropped_image)
                # 判断是否还有次数，没有次数的话就返回 （这里采用更复杂的逻辑，避免出现循环识图的情况）
                if "0" not in daily_competition_left_times_text:
                    # 选木星杯
                    self.d.click(360, 830)
                    time.sleep(DEFAULT_SLEEP_TIME)
                    continue
                else:
                    self.d.click(80, 1080)
                    time.sleep(DEFAULT_SLEEP_TIME)
                    continue

            # 如果是【每日竞赛】月光赏或者木星杯里面，选择具体难度的页面
            if np.all(screen[638, 50] == np.array([102, 153, 34])) and np.all(screen[638, 240] == np.array([102, 153, 34])):
                cropped_image = screen[11:37, 610:690]
                handler = ImageHandler()
                daily_competition_left_times_text = handler.get_text_from_image(self.ocr, cropped_image)
                # 判断是否还有次数，没有次数的话就返回 （这里采用更复杂的逻辑，避免出现循环识图的情况）
                if "0" not in daily_competition_left_times_text:
                    self.d.click(360, 700)
                    time.sleep(DEFAULT_SLEEP_TIME)
                    continue
                else:
                    self.d.click(80, 1080)
                    time.sleep(DEFAULT_SLEEP_TIME)
                    continue

            # 如果在【每日传奇竞赛】选择马娘的页面
            if np.all(screen[430, 360] == np.array([60, 205, 101])) and np.all(screen[460, 360] == np.array([106, 193, 129])):
                # 向下滑动，直到找到目标马娘为止
                sub_image = cv2.imread(self.dir + "/uma_icon/" + self.setting_dic["daily_legend_competition_oppenent_uma"] + ".png")
                handler = ImageHandler()
                best_match = handler.find_sub_image(sub_image, screen)
                if best_match is not None:
                    click_x, click_y = best_match["result"]
                    self.d.click(click_x, click_y)
                    time.sleep(DEFAULT_SLEEP_TIME)
                    continue
                else:
                    self.d.swipe(360, 720, 360, 520)
                    time.sleep(DEFAULT_SLEEP_TIME * 4)
                    continue

            # 如果都不是以上这些，则进入识图操作，查找类的需要判断逻辑
            sub_image_file_li = get_png_files(self.dir + "/find")
            for sub_image_file in sub_image_file_li:
                file_name_li = sub_image_file[0:-4].split("-")
                [click_x, click_y] = list(map(int, file_name_li[0].split(",")))
                [x0, x1, y0, y1] = list(map(int, file_name_li[1].split(",")))
                sub_image = cv2.imread(self.dir + "/find/" + sub_image_file)
                handler = ImageHandler()
                _match = handler.is_sub_image_in_box(sub_image, screen, x0 - 10, x1 + 10, y0 - 10, y1 + 10)
                if _match:
                    print(sub_image_file)
                    self.d.click(click_x, click_y)
                    time.sleep(DEFAULT_SLEEP_TIME)
                    continue

            # 如果都不是以上这些，则进入识图操作，点击类的不存在判断逻辑
            sub_image_file_li = get_png_files(self.dir + "/click")
            for sub_image_file in sub_image_file_li:
                sub_image = cv2.imread(self.dir + "/click/" + sub_image_file)
                handler = ImageHandler()
                best_match = handler.find_sub_image(sub_image, screen)
                if best_match is not None:
                    print(sub_image_file)
                    print(best_match["result"])
                    click_x, click_y = best_match["result"]
                    self.d.click(click_x, click_y)
                    time.sleep(DEFAULT_SLEEP_TIME)
                    continue

            # 如果是胜利结算出现【Tap】字样的页面
            cropped_image_1 = screen[1060:1120, 310:410]
            cropped_image_2 = screen[1040:1075, 310:410]
            handler = ImageHandler()
            k = handler.get_text_from_image(self.ocr, cropped_image_1)
            if k.lower() == "tap":
                self.d.click(360, 1110)
                time.sleep(DEFAULT_SLEEP_TIME)
                continue
            k = handler.get_text_from_image(self.ocr, cropped_image_2)
            if k.lower() == "tap":
                self.d.click(360, 1050)
                time.sleep(DEFAULT_SLEEP_TIME)
                continue


if __name__ == "__main__":
    _d = u2.connect("127.0.0.1:16384")
    _ocr = PaddleOCR(use_angle_cls=True)
    competition = Competition(_d, _ocr)
    competition.competition()

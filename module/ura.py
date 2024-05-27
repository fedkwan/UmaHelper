import time
import os
import importlib

import ddddocr
import uiautomator2 as u2
from paddleocr import PaddleOCR

from method.base import *
from module.cultivate.get_in_which_page import *
from module.cultivate.chose_scenario import *
from module.cultivate.chose_uma import *
from module.cultivate.chose_parent_uma import *
from module.cultivate.chose_support_card import *
from module.cultivate.get_round import *
from module.cultivate.get_status import *
from module.cultivate.train import *
from module.cultivate.add_skill import *


class Ura:

    def __init__(
        self,
        d: u2.connect,
        ocr: ddddocr.DdddOcr,
        p_ocr: PaddleOCR,
        setting_file="setting_1",
    ):
        self.dir = ROOT_DIR + "/resource/cultivate"
        self.d = d
        self.ocr = ocr
        self.p_ocr = p_ocr
        setting_data = importlib.import_module("customer_setting" + "." + setting_file)
        self.setting_dic = setting_data.data

    def pre_cultivate(self):
        screen = self.d.screenshot(format="opencv")

    def run(self):

        round_temp = -1

        while True:
            screen = self.d.screenshot(format="opencv")

            page = in_which_page(screen, self.ocr, self.p_ocr)
            if page is not None:
                print(page)

            # 首页则点击进入育成
            if page == "app_main":
                self.d.click(550, 1080)
                time.sleep(DEFAULT_SLEEP_TIME)
                continue

            if page == "chose_scenario":
                chose_scenario(self.d, self.setting_dic)
                time.sleep(DEFAULT_SLEEP_TIME)
                continue

            if page == "chose_uma":
                chose_uma(self.d, self.setting_dic)
                time.sleep(DEFAULT_SLEEP_TIME)
                continue

            if page == "chose_parent_uma":
                chose_parent_uma(self.d, self.setting_dic)
                time.sleep(DEFAULT_SLEEP_TIME)
                continue

            if page == "chose_support_card":
                chose_support_card(self.d, self.setting_dic)
                time.sleep(DEFAULT_SLEEP_TIME)
                continue

            if page == "main":
                # 识别不清楚就点开竞赛看
                if round_temp != -1:
                    round_num = round_temp
                else:
                    round_num = get_round(screen, self.p_ocr)
                    print(round_num)
                    if round_num == 2674:
                        round_num = competition_round_text_to_round_num(
                            self.d, self.p_ocr
                        )
                        round_temp = round_num
                print("round:" + str(round_num))
                # 历战最重要
                if self.setting_dic["schedule"][round_num] in [2, 3, 4]:
                    self.d.click(510, 1130)
                    time.sleep(DEFAULT_SLEEP_TIME)
                    continue

                # 然后是看病，看病不能用自动点击了，否则按照程序的运行逻辑会到最后才运行
                sub_image = cv2.imread(self.dir + "/find/clinic.png")
                image_matcher = ImageHandler()
                best_match = image_matcher.find_sub_image(sub_image, screen)
                if best_match:
                    self.d.click(140, 1155)
                    time.sleep(DEFAULT_SLEEP_TIME)
                    continue

                # 然后是外出和休息
                status_dic = get_status(screen)
                power = status_dic["power"]
                mood = status_dic["mood"]
                # 休息和外出（我觉得其实可以不用考虑合宿心情太差
                camp = [37, 38, 39, 40, 61, 62, 63, 64]
                if mood > 1 and power < 80:
                    if round_num in camp:
                        self.d.click(120, 990)
                        time.sleep(DEFAULT_SLEEP_TIME)
                        continue
                    else:
                        self.d.click(360, 1130)
                        time.sleep(DEFAULT_SLEEP_TIME)
                        continue
                elif power < 45:
                    self.d.click(120, 990)
                    time.sleep(DEFAULT_SLEEP_TIME)
                    continue

                # 都没事，就去训练
                self.d.click(360, 990)
                time.sleep(DEFAULT_SLEEP_TIME)
                continue

            if page == "train":
                round_temp = -1
                train(self.d, self.ocr, self.p_ocr, self.setting_dic)
                time.sleep(DEFAULT_SLEEP_TIME * 4)
                continue

            if page == "fans_require":
                self.d.click(200, 920)
                time.sleep(DEFAULT_SLEEP_TIME)
                continue

            if page == "target_times_require":
                self.d.click(200, 920)
                time.sleep(DEFAULT_SLEEP_TIME)
                continue

            if page == "consecutive_competition":
                self.d.click(520, 820)
                time.sleep(DEFAULT_SLEEP_TIME)
                continue

            if page == "target_competition_fans_require":
                self.d.click(200, 920)
                time.sleep(DEFAULT_SLEEP_TIME)
                continue

            if page == "event":
                self.d.click(360, 720)
                time.sleep(DEFAULT_SLEEP_TIME)
                continue

            if page == "competition":
                self.d.click(360, 1080)
                time.sleep(DEFAULT_SLEEP_TIME)
                continue
            if page == "competition_set_round":
                self.d.click(550, 1130)
                time.sleep(DEFAULT_SLEEP_TIME)
                continue
            if page == "competition_set_select":
                self.d.click(360, 1080)
                time.sleep(DEFAULT_SLEEP_TIME)
                continue

            if page == "competition_result":
                self.d.click(360, 1050)
                time.sleep(DEFAULT_SLEEP_TIME)
                continue

            if page == "inherit":
                self.d.click(360, 1050)
                time.sleep(DEFAULT_SLEEP_TIME)
                continue

            if page == "toy_grab":
                self.d.long_click(360, 1120, 1.5)
                time.sleep(DEFAULT_SLEEP_TIME)
                continue

            if page == "toy_grab_ok":
                self.d.click(360, 1180)
                time.sleep(DEFAULT_SLEEP_TIME)
                continue

            if page == "train_end":
                self.d.click(520, 1080)
                time.sleep(DEFAULT_SLEEP_TIME)
                continue

            if page == "train_end_add_skill":
                self.d.click(200, 1080)
                time.sleep(DEFAULT_SLEEP_TIME)
                continue

            if page == "skill":
                add_skill = AddSkill(self.d, self.p_ocr, self.setting_dic)
                add_skill.run()

            if page == "skill_add_end":
                self.d.click(80, 1180)
                time.sleep(DEFAULT_SLEEP_TIME)
                continue

            if page == "train_end_title":
                self.d.click(200, 830)
                time.sleep(DEFAULT_SLEEP_TIME)
                break

            # 如果都不是以上这些，则进入识图操作
            sub_image_file_li = get_png_files(self.dir + "/jam")
            for sub_image_file in sub_image_file_li:
                sub_image = cv2.imread(self.dir + "/jam/" + sub_image_file)
                matcher = ImageHandler()
                best_match = matcher.find_sub_image(sub_image, screen)
                if best_match is not None:
                    print(sub_image_file)
                    print(best_match["result"])
                    click_x, click_y = best_match["result"]
                    self.d.click(click_x, click_y)
                    time.sleep(DEFAULT_SLEEP_TIME)
                    continue

            # 如果都不是以上这些，则进入识图操作
            sub_image_file_li = get_png_files(self.dir + "/click")
            for sub_image_file in sub_image_file_li:
                sub_image = cv2.imread(self.dir + "/click/" + sub_image_file)
                matcher = ImageHandler()
                best_match = matcher.find_sub_image(sub_image, screen, 0.8)
                if best_match is not None:
                    print(sub_image_file)
                    print(best_match["result"])
                    click_x, click_y = best_match["result"]
                    self.d.click(click_x, click_y)
                    time.sleep(DEFAULT_SLEEP_TIME)
                    continue


if __name__ == "__main__":
    _d = u2.connect("127.0.0.1:16384")
    _ocr = ddddocr.DdddOcr()
    _p_ocr = PaddleOCR(use_angle_cls=True)
    ura = Ura(_d, _ocr, _p_ocr)
    ura.pre_cultivate()
    ura.run()

from method.recognition.imageMatcher import *
from method.recognition.textRecognizer import *
import uiautomator2 as u2
import ddddocr
import time
import numpy as np
from method.utils import *
import onnxruntime as ort


class Competition:
    def __init__(self, ocr: ddddocr.DdddOcr(), d: u2.connect()):
        self.ocr = ocr
        self.d = d
        self.resource_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/resource"

    def competition(self):

        _dir = self.resource_dir + "/competition"

        # 进入竞赛首页
        while True:

            screen = self.d.screenshot(format="opencv")
            # 定义一下资源文件夹，后面会用到

            # 如果是【游戏登录后】的首页
            # 定位底栏【主页面】蓝色
            if np.all(screen[1261, 360] == np.array([247, 159, 28])):
                self.d.click(520, 1220)
                time.sleep(DEFAULT_SLEEP_TIME)
                continue

            # 如果是【竞赛】的首页
            # 用4个方块的底部的灰线上的点的颜色来定位当前页面
            # 判断是不是每周结算时刻
            gray = np.array([109, 84, 89])
            _a, _b, _c, _d = screen[950, 320], screen[950, 400], screen[1106, 320], screen[1106, 400]
            if np.all(_a == _b) and np.all(_b == _c) and np.all(_c == _d) and np.all(_d == gray):
                # 判断第一格RP点槽是否为灰色，如果不是，说明还有RP点
                if np.all(screen[65, 430] != np.array([89, 76, 81])) and (is_monday_midnight_to_five() is False):
                    self.d.click(200, 850)
                    time.sleep(DEFAULT_SLEEP_TIME)
                    continue
                else:
                    self.d.click(200, 1050)
                    time.sleep(DEFAULT_SLEEP_TIME)
                    continue

            # 如果是【队伍竞技场】的首页
            # 用2个方块的底部的灰线上的点的颜色来定位当前页面
            _e, _f, weekend_gray = screen[875, 360], screen[1015, 360], np.array([70, 52, 57])
            # 判断是不是每周结算时刻
            if np.all(_e == weekend_gray) and np.all(_f == gray):
                self.d.click(80, 1080)
                time.sleep(DEFAULT_SLEEP_TIME)
                continue
            if np.all(_e == gray) and np.all(_f == gray):
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
            _g, _h, _i = screen[476, 360], screen[746, 360], screen[1016, 360]
            if np.all(_g == _h) and np.all(_h == _i) and np.all(_i == np.array([123, 91, 97])):
                self.d.click(360, 900)  # 选第3个
                time.sleep(DEFAULT_SLEEP_TIME)
                continue

            # 如果是【每日竞赛内容】的首页
            # 用2个方块的底部的灰线上的点的颜色来定位当前页面
            _j, _k = screen[1030, 200], screen[1030, 520]
            if np.all(_j == _k) and np.all(_k == gray):
                # 先看左边还有没有次数
                cropped_image = screen[835:855, 280:300]
                text_recognizer = TextRecognizer(cropped_image, self.ocr)
                daily_competition_left_times_text = text_recognizer.find_text_from_image()
                if daily_competition_left_times_text == "3":
                    self.d.click(210, 930)
                    time.sleep(DEFAULT_SLEEP_TIME)
                    continue
                # 再看右边有没有次数
                cropped_image = screen[835:855, 575:595]
                text_recognizer = TextRecognizer(cropped_image, self.ocr)
                daily_legend_competition_left_times_text = text_recognizer.find_text_from_image()
                if daily_legend_competition_left_times_text == "1":
                    self.d.click(510, 930)
                    time.sleep(DEFAULT_SLEEP_TIME)
                    continue
                # 如果都没次数，就退出循环了（后续如果要打传奇赛的话这里要改掉）
                if daily_competition_left_times_text != "3" and daily_legend_competition_left_times_text != "1":
                    self.d.click(360, 1220)  # 回到首页
                    print("竞赛结束")
                    time.sleep(DEFAULT_SLEEP_TIME)
                    break

            # 如果是【每日竞赛】，选择月光赏或者木星杯的页面
            part_image = cv2.imread(_dir + "/find/daily_competition_main.png")
            matcher = ImageMatcher(part_image, screen)
            match_result = matcher.find_part_image_from_total_image()
            if match_result is not None:
                cropped_image = screen[11:37, 620:642]
                text_recognizer = TextRecognizer(cropped_image, self.ocr)
                daily_competition_left_times_text = text_recognizer.find_text_from_image()
                print(daily_competition_left_times_text)
                # 判断是否还有次数，没有次数的话就返回 （这里采用更复杂的逻辑，避免出现循环识图的情况）
                if daily_competition_left_times_text == "3":
                    self.d.click(360, 830)
                    time.sleep(DEFAULT_SLEEP_TIME)
                    continue
                else:
                    self.d.click(80, 1080)
                    time.sleep(DEFAULT_SLEEP_TIME)
                    continue

            # 如果是【每日竞赛】月光赏或者木星杯里面，选择具体难度的页面
            part_image = cv2.imread(_dir + "/find/daily_competition_top.png")
            matcher = ImageMatcher(part_image, screen)
            match_result = matcher.find_part_image_from_total_image()
            if match_result is not None:
                cropped_image = screen[11:37, 620:642]
                text_recognizer = TextRecognizer(cropped_image, self.ocr)
                daily_competition_left_times_text = text_recognizer.find_text_from_image()
                print(daily_competition_left_times_text)
                # 判断是否还有次数，没有次数的话就返回 （这里采用更复杂的逻辑，避免出现循环识图的情况）
                if daily_competition_left_times_text == "3":
                    self.d.click(360, 830)
                    time.sleep(DEFAULT_SLEEP_TIME)
                    continue
                else:
                    self.d.click(80, 1080)
                    time.sleep(DEFAULT_SLEEP_TIME)
                    continue

            # 如果在【每日传奇竞赛】选择马娘的页面
            part_image = cv2.imread(_dir + "/find/daily_legend_competition_main.png")
            matcher = ImageMatcher(part_image, screen)
            match_result = matcher.is_part_image_in_box(375 - 10, 640 + 10, 145 - 10, 215 + 10)
            if match_result:
                # 向下滑动，直到找到目标马娘为止
                part_image = cv2.imread(_dir + "/find/qytk.png")
                temp = TemplateMatching(part_image, screen, threshold=0.9)
                best_match = temp.find_best_result()
                if best_match is not None:
                    center = best_match['result']
                    self.d.click(center[0], center[1])
                    time.sleep(DEFAULT_SLEEP_TIME)
                    continue
                else:
                    self.d.swipe(360, 720, 360, 520)
                    time.sleep(2)
                    continue

            # 如果是胜利结算出现【Tap】字样的页面
            cropped_image = screen[1060:1120, 310:410]
            text_recognizer = TextRecognizer(cropped_image, self.ocr)
            k = text_recognizer.find_text_from_image()
            if k.lower() == "tap":
                self.d.click(360, 1110)
                time.sleep(DEFAULT_SLEEP_TIME)
                continue

            # 如果是胜利结算出现【Tap】字样的页面
            cropped_image = screen[1040:1075, 310:410]
            text_recognizer = TextRecognizer(cropped_image, self.ocr)
            k = text_recognizer.find_text_from_image()
            if k.lower() == "tap":
                self.d.click(360, 1050)
                time.sleep(DEFAULT_SLEEP_TIME)
                continue

            # 如果都不是以上这些，则进入识图操作
            part_image_file_li = get_png_files(_dir)
            for part_image_file in part_image_file_li:
                file_name_li = part_image_file[0:-4].split("-")
                [click_x, click_y] = list(map(int, file_name_li[0].split(",")))
                [x0, x1, y0, y1] = list(map(int, file_name_li[1].split(",")))

                part_image = cv2.imread(_dir + "/" + part_image_file)
                matcher = ImageMatcher(part_image, screen)
                match_result = matcher.is_part_image_in_box(x0 - 10, x1 + 10, y0 - 10, y1 + 10)
                if match_result:
                    print(part_image_file)
                    self.d.click(click_x, click_y)
                    time.sleep(DEFAULT_SLEEP_TIME)
                    continue

            # 如果都不是以上这些，则进入识图操作
            part_image_file_li = get_png_files(self.resource_dir + "/general")
            for part_image_file in part_image_file_li:
                part_image = cv2.imread(self.resource_dir + "/general/" + part_image_file)
                matcher = ImageMatcher(part_image, screen, 0.7)
                match_result = matcher.find_part_image_from_total_image()
                if match_result is not None:
                    print(part_image_file)
                    print(match_result)
                    point = match_result["result"]
                    self.d.click(point[0], point[1])
                    time.sleep(DEFAULT_SLEEP_TIME)
                    continue

            # 如果都不是以上这些，则进入识图操作
            part_image_file_li = get_png_files(_dir + "/click")
            for part_image_file in part_image_file_li:
                part_image = cv2.imread(_dir + "/click/" + part_image_file)
                matcher = ImageMatcher(part_image, screen)
                match_result = matcher.find_part_image_from_total_image()
                if match_result is not None:
                    print(part_image_file)
                    print(match_result)
                    point = match_result["result"]
                    self.d.click(point[0], point[1])
                    time.sleep(DEFAULT_SLEEP_TIME)
                    continue


if __name__ == "__main__":
    ort.set_default_logger_severity(3)
    d = u2.connect("127.0.0.1:16384")
    ocr = ddddocr.DdddOcr()
    competition = Competition(ocr, d)
    competition.competition()

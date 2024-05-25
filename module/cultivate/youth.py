import time
import importlib
import uiautomator2 as u2
import ddddocr
import onnxruntime as ort
from paddleocr import PaddleOCR

from method.utils import *
from module.cultivate.get_in_which_page import *
from module.cultivate.get_round import *
from module.cultivate.train import *
from module.cultivate.add_skill import *


class Ura:

    def __init__(self, ocr: ddddocr.DdddOcr(), d: u2.connect(), uma_name):
        self.ocr = ocr
        self.d = d
        self.uma_name = uma_name
        self.resource_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/resource"

    def run(self):

        last_page = ""
        uma_name = "resource.uma_file" + "." + self.uma_name
        uma_model = importlib.import_module(uma_name)
        _ocr = PaddleOCR()

        while True:

            screen = self.d.screenshot(format="opencv")
            # 定义一下资源文件夹，后面会用到
            _dir = self.resource_dir + "/cultivate"

            page = in_which_page(screen, self.ocr, _dir)

            if page != last_page and page is not None:
                print(page)
                last_page = page

            time.sleep(DEFAULT_SLEEP_TIME * 2)

            if page == "app_main":
                self.d.click(550, 1080)
                time.sleep(DEFAULT_SLEEP_TIME)
                continue

            '''
            story_li = ["story_1", "story_2", "story_3", "story_4"]
            if page in story_li and page != "story_1":
                self.d.click(30, 585)
                time.sleep(DEFAULT_SLEEP_TIME)
                continue
            '''

            if page == "chose_uma":
                continue

            if page == "main":
                # 历战最重要
                try:
                    this_round = get_round(screen, self.ocr)
                    print(this_round)
                    print("==========")
                except Exception as e:
                    print(e)
                    continue

                if uma_model.data["schedule"][this_round] in [2, 3, 4]:
                    self.d.click(510, 1130)
                    time.sleep(DEFAULT_SLEEP_TIME)
                    continue

                # 然后是看病，看病不能用自动点击了，否则按照程序的运行逻辑会到最后才运行
                part_image = cv2.imread(_dir + "/find/clinic.png")
                image_matcher = ImageMatcher(part_image, screen)
                match_result = image_matcher.find_part_image_from_total_image()
                if match_result:
                    self.d.click(140, 1155)
                    time.sleep(DEFAULT_SLEEP_TIME)
                    continue

                # 获取体力值
                cropped_image = screen[161:162, 227:517]
                i = 0
                for pixel in cropped_image[0]:
                    if not np.all(pixel == [117, 117, 117]):
                        i += 1
                    else:
                        break
                power = round(i / 290 * 100)

                # 获取心情
                mood_list = [[105, 20, 241], [17, 90, 240], [3, 139, 207], [241, 105, 37], [206, 52, 140]]
                pixel_color = screen[140, 590].tolist()
                mood = mood_list.index(pixel_color) if pixel_color in mood_list else 6
                # 我觉得其实可以不用考虑合宿心情太差
                camp = [37, 38, 39, 40, 61, 62, 63, 64]
                if mood > 1 and power < 80:
                    if this_round in camp:
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
                self.d.click(360, 990)
                time.sleep(DEFAULT_SLEEP_TIME)
                continue

            if page == "train":
                train = Train(self.ocr, self.d, self.uma_name)
                train.train()
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
                _ocr = PaddleOCR()
                addskill = AddSkill(_ocr, d, "setting_1")
                addskill.run()

            if page == "skill_add_end":
                self.d.click(80, 1180)
                time.sleep(DEFAULT_SLEEP_TIME)
                continue

            if page == "train_end_title":
                self.d.click(200, 830)
                time.sleep(DEFAULT_SLEEP_TIME)
                break

            # 如果都不是以上这些，则进入识图操作
            part_image_file_li = get_png_files(_dir + "/click")
            for part_image_file in part_image_file_li:
                part_image = cv2.imread(_dir + "/click/" + part_image_file)
                matcher = ImageMatcher(part_image, screen)
                match_result = matcher.find_part_image_from_total_image()
                if match_result is not None:
                    print(part_image_file)
                    point = match_result["result"]
                    self.d.click(point[0], point[1])
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
                    point = match_result["result"]
                    self.d.click(point[0], point[1])
                    time.sleep(DEFAULT_SLEEP_TIME)
                    continue

    """
    task 有几个类型，识别画面，应当在画面静止1秒以上后再进行识别。
    一.cultivate
        1.休息 rest
        2.训练 train
        3.技能 skill
        4.看病 clinic
        5.外出 hangout
        6.竞赛 competition
        7.事件 event
        8.继承 归类在 jam 里面
    """


if __name__ == "__main__":
    ort.set_default_logger_severity(3)
    d = u2.connect("127.0.0.1:16384")
    ocr = ddddocr.DdddOcr()
    ura = Ura(ocr, d, "oguri_cap")
    ura.run()

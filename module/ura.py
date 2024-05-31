from module.cultivate.get_in_which_page import *
from module.cultivate.get_round import *
from module.cultivate.get_status import *
from module.cultivate.train import *
from module.cultivate.before_cultivate import *
from module.cultivate.cultivate_end import *


logging.getLogger("airtest").setLevel(logging.ERROR)
logging.getLogger("ppocr").setLevel(logging.ERROR)
logging.getLogger("ddddocr").setLevel(logging.ERROR)


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
        self.setting_dic = importlib.import_module(
            "customer_setting" + "." + setting_file
        ).data

    def run(self):

        last_ocr_round = -1
        while True:
            screen = self.d.screenshot(format="opencv")

            page = get_in_which_page(screen, self.ocr, self.p_ocr)
            if page is not None:
                print(page)

            if page == "main":
                # 识别不清楚就点开竞赛看

                if last_ocr_round == 2674:
                    this_round = competition_round_text_to_round_num(self.d, self.p_ocr)
                    last_ocr_round = this_round
                else:
                    this_round = get_round(screen, self.p_ocr)
                    if this_round == 2674:
                        last_ocr_round = this_round
                        continue
                print("round:" + str(this_round))

                # 历战最重要
                if self.setting_dic["schedule"][this_round] in [2, 3, 4]:
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

                # 都没事，就去训练
                self.d.click(360, 990)
                time.sleep(DEFAULT_SLEEP_TIME)
                continue

            if page == "train":
                round_temp = -1
                train(self.d, self.ocr, self.p_ocr, self.setting_dic)
                time.sleep(DEFAULT_SLEEP_TIME * 4)
                continue

            if page == "event":
                self.d.click(360, 720)
                time.sleep(DEFAULT_SLEEP_TIME)
                continue

            if page == "competition":
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

            if page == "app_main":
                before_cultivate(self.d, self.ocr, self.setting_dic)
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

            # 如果都不是以上这些，则进入识图操作，查找类的需要判断逻辑
            sub_image_file_li = get_png_files(self.dir + "/find_to_click")
            for sub_image_file in sub_image_file_li:
                file_name_li = sub_image_file[0:-4].split("-")
                [click_x, click_y] = list(map(int, file_name_li[0].split(",")))
                [x0, x1, y0, y1] = list(map(int, file_name_li[1].split(",")))
                sub_image = cv2.imread(self.dir + "/find_to_click/" + sub_image_file)
                handler = ImageHandler()
                _match = handler.is_sub_image_in_box(
                    sub_image, screen, x0 - 10, x1 + 10, y0 - 10, y1 + 10
                )
                if _match:
                    print(sub_image_file)
                    self.d.click(click_x, click_y)
                    time.sleep(DEFAULT_SLEEP_TIME)
                    continue


if __name__ == "__main__":
    _d = u2.connect("127.0.0.1:16384")
    _ocr = ddddocr.DdddOcr()
    _p_ocr = PaddleOCR(use_angle_cls=True)
    ura = Ura(_d, _ocr, _p_ocr, "setting_1")
    ura.run()

import time
import importlib
import uiautomator2 as u2

# import ddddocr
# from paddleocr import PaddleOCR
import numpy as np

from setting.base import *
from setting.ura_cultivate_page import *
from method.image_handler import *
from module.cultivate.chose_scenario import *

logging.getLogger("airtest").setLevel(logging.ERROR)

setting_dic = importlib.import_module("customer_setting.setting_1").data
dic = ura_cultivate_page_data

d = u2.connect("127.0.0.1:16384")
# ocr = ddddocr.DdddOcr()
# p_ocr = PaddleOCR(use_angle_cls=True)


def get_page_and_expect_list(screen: np.array, page_list: list):
    pages_to_check = page_list if len(page_list) != 0 else dic.keys()
    for page in pages_to_check:
        p = dic[page]["points"]
        count = sum(1 for pk, pv in p.items() if np.all(screen[pk] == np.array(pv)))
        if count == 4:
            _image = cv2.imread(ROOT_DIR + "/setting/page/" + page + ".png")
            handler = ImageHandler()
            match = handler.is_sub_image_in_box2(
                _image, screen, dic[page]["sub_image_position"]
            )
            if match:
                return page


def page_action(page):
    if page == "app_main":
        d.click(550, 1080)
        time.sleep(DEFAULT_SLEEP_TIME)

    if page == "chose_scenario":
        chose_scenario(d, setting_dic)
        d.click(360, 1080)
        time.sleep(DEFAULT_SLEEP_TIME * 6)

page_list = []
while True:
    screen = d.screenshot(format="opencv")
    page = get_page_and_expect_list(screen, page_list)
    if page is None:
        continue
    page_list = dic[page]["expect_page_list"]

    print(page)
    print(page_list)

    page_action(page)

    time.sleep(DEFAULT_SLEEP_TIME)

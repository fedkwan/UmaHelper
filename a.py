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
from module.cultivate.chose_uma import *
from module.cultivate.chose_parent_uma import *
from module.cultivate.chose_support_card import *

logging.getLogger("airtest").setLevel(logging.ERROR)
logging.getLogger("ppocr").setLevel(logging.ERROR)
logging.getLogger("ddddocr").setLevel(logging.ERROR)


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
            
def check_click(d: u2.connect):
    # 如果都不是以上这些，则进入识图操作
    sub_image_file_li = get_png_files(ROOT_DIR + "/setting/click")
    for sub_image_file in sub_image_file_li:
        sub_image = cv2.imread(ROOT_DIR + "/setting/click/" + sub_image_file)
        matcher = ImageHandler()
        best_match = matcher.find_sub_image(sub_image, screen, 0.8)
        if best_match is not None:
            print(sub_image_file)
            print(best_match["result"])
            click_x, click_y = best_match["result"]
            d.click(click_x, click_y)
            time.sleep(DEFAULT_SLEEP_TIME)
            continue


def page_action(page):
    if page == "app_main":
        d.click(550, 1080)
        time.sleep(DEFAULT_SLEEP_TIME * 2)

    if page == "chose_scenario":
        chose_scenario(d, setting_dic)
        d.click(360, 1080)
        time.sleep(DEFAULT_SLEEP_TIME * 6)

    if page == "chose_uma":
        chose_uma(d, setting_dic)
        d.click(360, 1080)
        time.sleep(DEFAULT_SLEEP_TIME * 6)

    if page == "chose_parent_uma":
        chose_parent_uma(d, setting_dic)
        d.click(360, 1080)
        time.sleep(DEFAULT_SLEEP_TIME * 6)

    if page == "chose_support_card":
        chose_support_card(d, setting_dic)
        d.click(360, 1080)
        time.sleep(DEFAULT_SLEEP_TIME * 6)


setting_dic = importlib.import_module("customer_setting.setting_1").data
dic = ura_cultivate_page_data

d = u2.connect("127.0.0.1:16384")
# ocr = ddddocr.DdddOcr()
# p_ocr = PaddleOCR(use_angle_cls=True)

page_list = []
jam = 0
while True:
    screen = d.screenshot(format="opencv")

    page = get_page_and_expect_list(screen, page_list)
    print(page)
    if page is None:
        check_click(d)
        continue

    page_action(page)
    print(page + " action done")

    except_page_list = dic[page]["expect_page_list"]
    print(except_page_list)

    check_click(d)
    

    time.sleep(DEFAULT_SLEEP_TIME * 2)

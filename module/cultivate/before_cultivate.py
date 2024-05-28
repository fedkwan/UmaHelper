import importlib

import uiautomator2 as u2
import numpy as np

from method.base import *
from method.utils import *
from method.image_handler import *
from module.cultivate.chose_scenario import *
from module.cultivate.chose_uma import *
from module.cultivate.chose_parent_uma import *
from module.cultivate.chose_support_card import *

logging.getLogger("airtest").setLevel(logging.ERROR)
logging.getLogger("ppocr").setLevel(logging.ERROR)
logging.getLogger("ddddocr").setLevel(logging.ERROR)


def before_cultivate(d: u2.connect, ocr: ddddocr.DdddOcr, setting_dic: dict):

    while True:

        screen = d.screenshot(format="opencv")

        # 通过底部栏【主页面】的3个蓝色，加上【礼物】按钮的1个红色，判断是否游戏主界面
        if (
            np.all(screen[1264, 300] == np.array([220, 130, 0]))
            and np.all(screen[1264, 360] == np.array([220, 130, 0]))
            and np.all(screen[1264, 420] == np.array([220, 130, 0]))
            and np.all(screen[920, 650] == np.array([102, 68, 221]))
        ):
            # 识别左下角【商店】图标，再次 确认判断
            _image = cv2.imread(
                ROOT_DIR + "/resource/before_cultivate/find/main_shop.png"
            )
            handler = ImageHandler()
            match = handler.is_sub_image_in_box(_image, screen, 220, 270, 1070, 1110)
            if match:
                print("page:::当前为游戏主页面。")

                # 点击进入培育
                d.click(550, 1080)
                time.sleep(DEFAULT_SLEEP_TIME)
                continue

        # 通过底部【滑动栏】的4个棕色点，判断是否选剧本界面
        scenario_brown = np.array([22, 64, 121])
        scenario_green = np.array([24, 222, 156])
        if (
            (
                np.all(screen[1016, 316] == scenario_brown)
                or np.all(screen[1016, 316] == scenario_green)
            )
            and (
                np.all(screen[1016, 345] == scenario_brown)
                or np.all(screen[1016, 345] == scenario_green)
            )
            and (
                np.all(screen[1016, 375] == scenario_brown)
                or np.all(screen[1016, 375] == scenario_green)
            )
            and (
                np.all(screen[1016, 404] == scenario_brown)
                or np.all(screen[1016, 404] == scenario_green)
            )
        ):
            # 识别右上角【剧本记录】4个字，再次 确认判断
            _image = cv2.imread(
                ROOT_DIR + "/resource/before_cultivate/find/scenario_record.png"
            )
            handler = ImageHandler()
            match = handler.is_sub_image_in_box(_image, screen, 527, 620, 127, 157)
            if match:
                print("page:::当前为剧本选择页。")

                chose_scenario(d, setting_dic)
                d.click(360, 1080)
                time.sleep(DEFAULT_SLEEP_TIME * 6)
                continue

        # 通过五维属性栏【速度】【力量】【智力】内的3个绿色，加上【马娘星星数】的第1个星星的黄色，判断是否选择马娘页
        light_green = np.array([36, 217, 121])
        if (
            np.all(screen[460, 150] == light_green)
            and np.all(screen[460, 410] == light_green)
            and np.all(screen[460, 670] == light_green)
            and np.all(screen[367, 64] == np.array([34, 204, 255]))
        ):
            # 识别右上角【培育咨询】4个字，再次 确认判断
            _image = cv2.imread(
                ROOT_DIR + "/resource/before_cultivate/find/cultivate_info.png"
            )
            handler = ImageHandler()
            match = handler.is_sub_image_in_box(_image, screen, 470, 563, 402, 432)
            if match:
                print("page:::当前为马娘选择页。")
                chose_uma(d, setting_dic)
                d.click(360, 1080)
                time.sleep(DEFAULT_SLEEP_TIME * 6)
                continue

        # 通过五维属性栏【速度】【力量】【智力】内的3个绿色，加上右上方【契合度】的橙色，判断是否选择种马页
        if (
            np.all(screen[460, 150] == light_green)
            and np.all(screen[460, 410] == light_green)
            and np.all(screen[460, 670] == light_green)
            and np.all(screen[180, 520] == np.array([80, 144, 255]))
        ):
            # 种马选择框【第2位】的3个字，再次 确认判断
            _image = cv2.imread(
                ROOT_DIR + "/resource/before_cultivate/find/parent_uma_second.png"
            )
            handler = ImageHandler()
            match = handler.is_sub_image_in_box(_image, screen, 382, 447, 654, 678)
            if match:
                print("page:::当前为种马选择页。")
                chose_parent_uma(d, setting_dic)
                d.click(360, 1080)
                time.sleep(DEFAULT_SLEEP_TIME * 6)
                continue

        # 通过上方【牌组标题栏】的2个绿色，加上右下方【好友卡位】的加号的绿色和底栏2个粉色判断是否支援卡选择页
        if (
            np.all(screen[240, 40] == np.array([73, 201, 73]))
            and np.all(screen[240, 480] == np.array([73, 201, 73]))
            and np.all(screen[790, 480] == np.array([162, 102, 255]))
            and np.all(screen[790, 660] == np.array([162, 102, 255]))
        ):
            # 识别右上角【培育咨询】4个字，再次 确认判断
            _image = cv2.imread(
                ROOT_DIR + "/resource/before_cultivate/find/support_card_copy.png"
            )
            handler = ImageHandler()
            match = handler.is_sub_image_in_box(_image, screen, 587, 645, 229, 260)
            if match:
                print("page:::当前为支援卡选择页。")
                chose_support_card(d, setting_dic)
                time.sleep(DEFAULT_SLEEP_TIME * 6)
                break

        # 如果都不是以上这些，则进入识图操作，后面会替换成列表形式，不再需要遍历文件夹
        sub_image_file_li = get_png_files(ROOT_DIR + "/resource/before_cultivate/click")
        for sub_image_file in sub_image_file_li:
            sub_image = cv2.imread(
                ROOT_DIR + "/resource/before_cultivate/click/" + sub_image_file
            )
            handler = ImageHandler()
            best_match = handler.find_sub_image(sub_image, screen, 0.8)
            if best_match is not None:
                click_x, click_y = best_match["result"]
                d.click(click_x, click_y)
                print("click:::当前点击了" + sub_image_file)
                time.sleep(DEFAULT_SLEEP_TIME)
                continue

        time.sleep(DEFAULT_SLEEP_TIME)


# test
if __name__ == "__main__":
    _d = u2.connect("127.0.0.1:16384")
    _ocr = ddddocr.DdddOcr()
    _setting_dic = importlib.import_module("customer_setting.setting_1").data
    before_cultivate(_d, _ocr, _setting_dic)

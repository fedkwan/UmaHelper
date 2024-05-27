import importlib

import uiautomator2 as u2

from method.base import *
from method.utils import *
from method.image_handler import *


def chose_support_card(d: u2.connect, setting_dic: dict):
    support_card_name = setting_dic["support_card_png_name"]
    png_path = ROOT_DIR + "/resource/support_card/" + support_card_name
    sub_image = cv2.imread(png_path)

    while True:
        screen = d.screenshot(format="opencv")

        # 牌组标题栏的绿色
        if np.all(screen[240, 480] == np.array([73, 201, 73])):

            # 支援卡的加号在不在，在的话点击进去
            if np.all(screen[679, 571] == np.array([23, 219, 153])):
                d.click(571, 679)
                time.sleep(DEFAULT_SLEEP_TIME)

            # 不在的话说明搞定了，开始培育
            else:
                d.click(360, 1080)
                time.sleep(DEFAULT_SLEEP_TIME * 2)

        # 选择好友支援 / 最后确认 的标题栏都是这样的
        if np.all(screen[40, 360] == np.array([8, 215, 146])) and np.all(screen[85, 360] == np.array([12, 195, 109])):

            # 用确认页面 消耗金币 底下的绿色来判断，这里是选择好友支援
            if np.all(screen[1060, 60] != np.array([73, 201, 73])):
                handler = ImageHandler()
                best_match = handler.find_sub_image(sub_image, screen, 0.7)

                # 最好是按 关注 + 最后登入 升序 来排列，提前关注好想要用的支援卡的好友
                if best_match is not None:
                    click_x, click_y = best_match["result"]
                    d.click(click_x, click_y)
                    time.sleep(DEFAULT_SLEEP_TIME)

                # 没找到就向下滑动一下
                else:
                    d.swipe(360, 900, 360, 300)
                    time.sleep(DEFAULT_SLEEP_TIME)

            # 如果是最后确认，就直接开始培育
            else:
                d.click(530, 1180)
                break


# test
if __name__ == "__main__":
    _d = u2.connect("127.0.0.1:16384")
    _setting_dic = importlib.import_module("customer_setting.setting_1").data
    chose_support_card(_d, _setting_dic)

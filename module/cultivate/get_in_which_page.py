import numpy as np

from method.base import *
from method.utils import *
from method.image_handler import *
from method.text_handler import *


def in_which_page(screen: np.array, ocr: PaddleOCR(), d_ocr: ddddocr.DdddOcr(), jam: bool = False):
    # 这些都是只会触发一次的，考虑在屏幕卡住的时候再去判断是否需要触发，节约资源
    if jam:
        # 如果是【游戏登录后】的首页
        # 点进培育
        if np.all(screen[1261, 360] == np.array([247, 159, 28])) and np.all(screen[920, 650] == np.array([102, 68, 221])):
            return "app_main"

        # 选剧本
        brown = np.array([24, 222, 156])
        if np.all(screen[1016, 316] == brown) or np.all(screen[1016, 345] == brown) or np.all(screen[1016, 375] == brown) or np.all(
                screen[1016, 404] == brown):
            return "chose_scenario"

        # 选马娘 / 选种马 先使用 1、3、5 三个点
        # attribute_point_2 = screen[460, 280]
        # attribute_point_4 = screen[460, 540]
        light_green = np.array([36, 217, 121])
        if np.all(screen[460, 150] == light_green) and np.all(screen[460, 410] == light_green) and np.all(screen[460, 670] == light_green):

            # 用第1位、第2位的蓝色、粉色来判断是选马娘还是选种马的页面
            if np.all(screen[660, 110] == np.array([247, 179, 36])):
                return "chose_parent_uma"
            else:
                return "chose_uma"

        # 选支援卡
        if np.all(screen[240, 480] == np.array([73, 201, 73])):
            return "chose_support_card"

    # 根据五维属性的顶栏的颜色是不是相等，判断当前是不是培育主界面 / 训练界面
    if np.all(screen[853, 120] == screen[906, 350]) and np.all(screen[853, 350] == screen[906, 580]):
        # 根据技能按钮底部的粉蓝色判断是不是培育主界面
        if np.all(screen[1020, 550] == np.array([215, 195, 43])):
            return "main"

    # 判断是否训练页面
    cropped_image = screen[207:229, 99:204]
    handler = ImageHandler()
    train_type_text = handler.get_text_from_image(ocr, cropped_image)[0:2]
    train_type_li = ["速度", "持久", "力量", "意志", "智力"]
    if train_type_text in train_type_li:
        return "train"

    if np.all(screen[580, 36] == np.array([134, 126, 255])) and np.all(screen[560, 36] == np.array([134, 126, 255])):
        return "competition"

    if np.all(screen[420, 320] == np.array([40, 211, 158])) and np.all(screen[420, 460] == np.array([40, 211, 158])):
        return "skill"

    """
    # 根据左上角的title和右下角的重置 判断 当前是否加技能界面
    skill_title_cropped_image = screen[10:34, 20:120]
    # cv2.imwrite("cut" + str(time.time()) + ".png", skill_title_cropped_image)
    skill_title_text_recognizer = TextRecognizer(skill_title_cropped_image, ocr)
    skill_title_text = skill_title_text_recognizer.find_text_from_image()

    skill_reset_cropped_image = screen[1065:1095, 560:680]
    # cv2.imwrite("cut" + str(time.time()) + ".png", skill_reset_cropped_image)
    skill_reset_text_recognizer = TextRecognizer(skill_reset_cropped_image, ocr)
    skill_reset_text = skill_reset_text_recognizer.find_text_from_image()

    if ("技能" in skill_title_text) and (skill_reset_text == "重置"):
        inherit_cropped_image = screen[406:436, 530:630]
        inherit_text_recognizer = TextRecognizer(inherit_cropped_image, ocr)
        inherit_text = inherit_text_recognizer.find_text_from_image()
        inherit_num = find_numbers_in_string(inherit_text, "rude")
        if inherit_num < 100:
            return "skill_add_end"
        else:
            return "skill"

    """
    # 根据是否出现两个选项马蹄铁图片 判断 当前是否事件界面
    event_green_image = cv2.imread(ROOT_DIR + "/resource/cultivate/find/event_green.png")
    event_yellow_image = cv2.imread(ROOT_DIR + "/resource/cultivate/find/event_yellow.png")
    handler = ImageHandler()
    event_green_match = handler.is_sub_image_in_box(event_green_image, screen, 30, 70, 0, 1280)
    event_yellow_match = handler.is_sub_image_in_box(event_yellow_image, screen, 30, 70, 0, 1280)
    if event_green_match and event_yellow_match:
        return "event"

    cropped_image = screen[1040:1075, 310:410]
    handler = ImageHandler()
    k = handler.get_text_from_image_dddd(d_ocr, cropped_image)
    if k.lower() == "tap":
        return "competition_result"

    # 继承因子
    inherit_cropped_image = screen[1028:1075, 266:345]
    handler = ImageHandler()
    inherit_text = handler.get_text_from_image_dddd(d_ocr, inherit_cropped_image)
    if inherit_text == "因子":
        return "inherit"

    fans_require_image = cv2.imread(ROOT_DIR + "/resource/cultivate/find/fans_require.png")
    handler = ImageHandler()
    fans_require_match = handler.is_sub_image_in_box(fans_require_image, screen, 247, 476, 310, 350)
    if fans_require_match:
        return "fans_require"

    fans_require_image = cv2.imread(ROOT_DIR + "/resource/cultivate/find/target_times_require.png")
    handler = ImageHandler()
    fans_require_match = handler.is_sub_image_in_box(fans_require_image, screen, 230, 492, 310, 350)
    if fans_require_match:
        return "target_times_require"

    fans_require_image = cv2.imread(ROOT_DIR + "/resource/cultivate/find/consecutive_competition.png")
    handler = ImageHandler()
    fans_require_match = handler.is_sub_image_in_box(fans_require_image, screen, 292, 428, 393, 434)
    if fans_require_match:
        return "consecutive_competition"

    fans_require_image = cv2.imread(ROOT_DIR + "/resource/cultivate/find/target_competition_fans_require.png")
    handler = ImageHandler()
    fans_require_match = handler.is_sub_image_in_box(fans_require_image, screen, 215, 508, 309, 350)
    if fans_require_match:
        return "target_competition_fans_require"

    fans_require_image = cv2.imread(ROOT_DIR + "/resource/cultivate/find/toy_grab.png")
    handler = ImageHandler()
    fans_require_match = handler.find_sub_image(fans_require_image, screen, 0.8)
    if fans_require_match:
        return "toy_grab"

    fans_require_image = cv2.imread(ROOT_DIR + "/resource/cultivate/find/toy_grab_ok.png")
    handler = ImageHandler()
    fans_require_match = handler.is_sub_image_in_box(fans_require_image, screen, 333, 386, 1168, 1202)
    if fans_require_match:
        return "toy_grab_ok"

    train_end_image = cv2.imread(ROOT_DIR + "/resource/cultivate/find/train_end.png")
    handler = ImageHandler()
    train_end_match = handler.is_sub_image_in_box(train_end_image, screen, 445, 561, 1065, 1105)

    inherit_cropped_image = screen[1078:1098, 232:289]
    handler = ImageHandler()
    inherit_text = handler.get_text_from_image(d_ocr, inherit_cropped_image)
    inherit_num = find_numbers_in_string(inherit_text, "rude")
    if train_end_match:
        if inherit_num < 100:
            return "train_end"
        else:
            return "train_end_add_skill"

    fans_require_image = cv2.imread(ROOT_DIR + "/resource/cultivate/find/train_end_title.png")
    handler = ImageHandler()
    fans_require_match = handler.is_sub_image_in_box(fans_require_image, screen, 292, 428, 394, 434)
    if fans_require_match:
        return "train_end_title"

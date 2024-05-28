import numpy as np

from method.base import *
from method.utils import *
from method.image_handler import *
from method.text_handler import *


def in_which_page(screen: np.array, ocr: ddddocr.DdddOcr, p_ocr: PaddleOCR):

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
                return "app_main"

    # 根据五维属性的顶栏的颜色是不是相等，判断当前是不是培育主界面 / 训练界面
    if np.all(screen[853, 120] == screen[906, 350]) and np.all(
        screen[853, 350] == screen[906, 580]
    ):
        # 根据技能按钮底部的粉蓝色判断是不是培育主界面
        if np.all(screen[1020, 550] == np.array([215, 195, 43])):
            return "main"

        else:
            # 判断是否训练页面
            cropped_image = screen[207:229, 99:204]
            handler = ImageHandler()
            train_type_text = handler.get_text_from_image(ocr, cropped_image)[0:2]
            train_type_li = ["速度", "持久", "力量", "意志", "智力"]
            if train_type_text in train_type_li:
                return "train"

    if np.all(screen[580, 36] == np.array([134, 126, 255])) and np.all(
        screen[560, 36] == np.array([134, 126, 255])
    ):
        return "competition"

    # 根据是否出现两个选项马蹄铁图片 判断 当前是否事件界面
    event_green_image = cv2.imread(
        ROOT_DIR + "/resource/cultivate/find/event_green.png"
    )
    event_yellow_image = cv2.imread(
        ROOT_DIR + "/resource/cultivate/find/event_yellow.png"
    )
    handler = ImageHandler()
    event_green_match = handler.is_sub_image_in_box(
        event_green_image, screen, 30, 70, 0, 1280
    )
    event_yellow_match = handler.is_sub_image_in_box(
        event_yellow_image, screen, 30, 70, 0, 1280
    )
    if event_green_match and event_yellow_match:
        return "event"

    cropped_image = screen[1040:1075, 310:410]
    handler = ImageHandler()
    k = handler.get_text_from_image(ocr, cropped_image)
    if k.lower() == "tap":
        return "competition_result"

    # 继承因子
    inherit_cropped_image = screen[1028:1075, 266:345]
    handler = ImageHandler()
    inherit_text = handler.get_text_from_image(ocr, inherit_cropped_image)
    if inherit_text == "因子":
        return "inherit"

    fans_require_image = cv2.imread(
        ROOT_DIR + "/resource/cultivate/find/fans_require.png"
    )
    handler = ImageHandler()
    fans_require_match = handler.is_sub_image_in_box(
        fans_require_image, screen, 247, 476, 310, 350
    )
    if fans_require_match:
        return "fans_require"

    fans_require_image = cv2.imread(
        ROOT_DIR + "/resource/cultivate/find/target_times_require.png"
    )
    handler = ImageHandler()
    fans_require_match = handler.is_sub_image_in_box(
        fans_require_image, screen, 230, 492, 310, 350
    )
    if fans_require_match:
        return "target_times_require"

    fans_require_image = cv2.imread(
        ROOT_DIR + "/resource/cultivate/find/consecutive_competition.png"
    )
    handler = ImageHandler()
    fans_require_match = handler.is_sub_image_in_box(
        fans_require_image, screen, 292, 428, 393, 434
    )
    if fans_require_match:
        return "consecutive_competition"

    fans_require_image = cv2.imread(
        ROOT_DIR + "/resource/cultivate/find/target_competition_fans_require.png"
    )
    handler = ImageHandler()
    fans_require_match = handler.is_sub_image_in_box(
        fans_require_image, screen, 215, 508, 309, 350
    )
    if fans_require_match:
        return "target_competition_fans_require"

    fans_require_image = cv2.imread(ROOT_DIR + "/resource/cultivate/find/toy_grab.png")
    handler = ImageHandler()
    fans_require_match = handler.find_sub_image(fans_require_image, screen, 0.8)
    if fans_require_match:
        return "toy_grab"

    fans_require_image = cv2.imread(
        ROOT_DIR + "/resource/cultivate/find/toy_grab_ok.png"
    )
    handler = ImageHandler()
    fans_require_match = handler.is_sub_image_in_box(
        fans_require_image, screen, 333, 386, 1168, 1202
    )
    if fans_require_match:
        return "toy_grab_ok"

    # 通过【基础能力】【场地资质】【距离资质】【脚质资质】的颜色，初步 判断是否是培育结束页面
    if (
        np.all(screen[340, 356] == np.array([36, 217, 121]))
        and np.all(screen[610, 356] == np.array([36, 217, 121]))
        and np.all(screen[650, 356] == np.array([36, 217, 121]))
        and np.all(screen[730, 356] == np.array([36, 217, 121]))
    ):

        # 识别右下角【培养结束】4个字，再次 确认判断
        _image = cv2.imread(ROOT_DIR + "/resource/after_cultivate/find/train_end.png")
        handler = ImageHandler()
        match = handler.is_sub_image_in_box(_image, screen, 445, 561, 1065, 1105)
        if match:
            return "train_end"

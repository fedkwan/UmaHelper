import uiautomator2 as u2
from paddleocr import PaddleOCR
import numpy as np

from module.cultivate.get_round import *
from module.cultivate.get_status import *

cultivate_dir = ROOT_DIR + "/resource/cultivate"

def cultivate_main(d: u2.connect, p_ocr: PaddleOCR, setting_dic: dict):

    screen = d.screenshot(format="opencv")
    this_round = get_round(screen, p_ocr)
    print("round:" + str(this_round))

    # 历战最重要
    if setting_dic["schedule"][this_round] in [2, 3, 4]:
        d.click(510, 1130)
        time.sleep(DEFAULT_SLEEP_TIME * 6)

    # 然后是看病，看病不能用自动点击了，否则按照程序的运行逻辑会到最后才运行
    sub_image = cv2.imread(cultivate_dir + "/find/clinic.png")
    image_matcher = ImageHandler()
    best_match = image_matcher.find_sub_image(sub_image, screen)
    if best_match:
        d.click(140, 1155)
        time.sleep(DEFAULT_SLEEP_TIME)

    # 然后是外出和休息
    status_dic = get_status(screen)
    power = status_dic["power"]
    mood = status_dic["mood"]
    # 休息和外出（我觉得其实可以不用考虑合宿心情太差
    camp = [37, 38, 39, 40, 61, 62, 63, 64]
    if mood > 1 and power < 80:
        if this_round in camp:
            d.click(120, 990)
            time.sleep(DEFAULT_SLEEP_TIME)
        else:
            d.click(360, 1130)
            time.sleep(DEFAULT_SLEEP_TIME)
    elif power < 45:
        d.click(120, 990)
        time.sleep(DEFAULT_SLEEP_TIME)

    # 都没事，就去训练
    d.click(360, 990)
    time.sleep(DEFAULT_SLEEP_TIME)

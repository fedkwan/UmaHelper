import cv2
import uiautomator2 as u2
import ddddocr
import numpy as np
from method.recognition.textRecognizer import *
from paddleocr import PaddleOCR, draw_ocr


def add_skill(d: u2.connect(), ocr: ddddocr.DdddOcr()):
    screen = d.screenshot(format="opencv")

    i = 0
    for i in range(472, 1280):
        if np.all(screen[i, 360] != np.array([255, 255, 255])):
            print(i)
            break


def fix_swipe(d: u2.connect()):
    screen = d.screenshot(format="opencv")
    i = 0
    for i in range(472, 1280):
        if np.all(screen[i, 360] != np.array([255, 255, 255])):
            break
    print(i)

    gap = i - 472

    d.swipe(360, 900, 360, 900 - gap * 1.8)


def get_box_skill_text(screen: np.ndarray, ocr: ddddocr.DdddOcr()):
    # 获取当前屏幕内技能方框的纵坐标组
    y_li = []
    i = 472  # 472 到 1028 是技能列表的范围
    while i < 1028:
        if np.all(screen[i, 360] == np.array([210, 193, 193])):
            if i + 52 < 1028:
                y_li.append(i)
            i += 155
        else:
            i += 1

    ocr = PaddleOCR(use_angle_cls=True, lang="chinese_cht")
    text_li = []

    for y in y_li:
        cropped_image = screen[y:y + 52, 138:482]
        cv2.imwrite(str(y) + ".png", cropped_image)

        result = ocr.ocr(cropped_image, cls=True)
        for idx in range(len(result)):
            res = result[idx]
            # for line in res:
            print(res)

        # text_recognizer = TextRecognizer(cropped_image, ocr)
        # text = text_recognizer.find_text_from_image()
        # text_li.append(text)

    return text_li


# test
if __name__ == "__main__":
    _d = u2.connect("127.0.0.1:16384")
    _ocr = ddddocr.DdddOcr()

    # _d.swipe(360, 1000, 360, 520, 1)

    _screen = _d.screenshot(format="opencv")
    g = get_box_skill_text(_screen, _ocr)

    print(g)

    # add_skill(_d, _ocr)

    # fix_swipe(_d)

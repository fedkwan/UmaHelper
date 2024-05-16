import uiautomator2 as u2
import ddddocr
import numpy as np


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


# test
if __name__ == "__main__":
    _d = u2.connect("127.0.0.1:16384")
    _ocr = ddddocr.DdddOcr()

    # _d.swipe(360, 920, 360, 556)

    # add_skill(_d, _ocr)

    fix_swipe(_d)

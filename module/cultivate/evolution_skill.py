import time
import uiautomator2 as u2

from setting.base import *
from method.utils import *


def evolution_skill(d):

    while True:
        screen = d.screenshot(format="opencv")

        for y in range(104, 1040):
            if (
                np.all(screen[y, 235] == np.array([186, 116, 255]))
                and np.all(screen[y, 234] == np.array([235, 219, 255]))
                and np.all(screen[y + 33, 64] != np.array([37, 212, 140]))
            ):
                d.click(64, y + 33)
        d.swipe(360, 900, 360, 500, 0.8)

        # 滑动到底部
        if np.all(screen[1022, 695] == np.array([142, 120, 125])):
            d.click(520, 1180)
            break
        time.sleep(DEFAULT_SLEEP_TIME * 2)


# test
if __name__ == "__main__":
    _d = u2.connect("127.0.0.1:16384")
    evolution_skill(_d)

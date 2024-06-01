from method.image_handler import *
from module.cultivate.add_skill import *

logging.getLogger("airtest").setLevel(logging.ERROR)
logging.getLogger("ppocr").setLevel(logging.ERROR)
logging.getLogger("ddddocr").setLevel(logging.ERROR)


def destroy_account(d: u2.connect):

    print("xxxx")

    while True:

        screen = d.screenshot(format="opencv")

        # 滑动到底部
        if np.all(screen[1098, 696] == np.array([142, 120, 125])):
            d.click(360, 1050)
            time.sleep(DEFAULT_SLEEP_TIME * 2)
            break

        d.swipe(360, 1000, 360, 200, 0.2)
    
# test
if __name__ == "__main__":
    _d = u2.connect("127.0.0.1:16384")
    destroy_account(_d)
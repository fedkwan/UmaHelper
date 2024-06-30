from method.image_handler import *
from module.cultivate.add_skill import *

logging.getLogger("airtest").setLevel(logging.ERROR)
logging.getLogger("ppocr").setLevel(logging.ERROR)
logging.getLogger("ddddocr").setLevel(logging.ERROR)


def cultivate_end(d: u2.connect, ocr: ddddocr.DdddOcr):

    screen = d.screenshot(format="opencv")

    # 截取左下角【技能】处的技能Pt值，判断是否低于100
    cropped_image = screen[1078:1098, 232:289]
    handler = ImageHandler()
    text = handler.get_text_from_image(ocr, cropped_image)
    num = find_numbers_in_string(text, "rude")

    # 如果小于 100，就说明没什么技能可以加了，点击【培育结束】
    if num > 100:
        d.click(200, 1080)
        time.sleep(DEFAULT_SLEEP_TIME * 6)
        return
    else:
        d.click(520, 1080)
        time.sleep(DEFAULT_SLEEP_TIME * 6)


# test
if __name__ == "__main__":
    _d = u2.connect("127.0.0.1:16384")
    _ocr = ddddocr.DdddOcr()
    _p_ocr = PaddleOCR(use_angle_cls=True)
    _setting_dic = importlib.import_module("customer_setting.setting_1").data
    cultivate_end(_d, _ocr)

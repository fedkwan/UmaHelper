from method.image_handler import *
from module.cultivate.add_skill import *

logging.getLogger("airtest").setLevel(logging.ERROR)
logging.getLogger("ppocr").setLevel(logging.ERROR)
logging.getLogger("ddddocr").setLevel(logging.ERROR)


def cultivate_end(
    d: u2.connect, ocr: ddddocr.DdddOcr
):

    screen = d.screenshot(format="opencv")

    # 截取左下角【技能】处的技能Pt值，判断是否低于100
    cropped_image = screen[1078:1098, 232:289]
    handler = ImageHandler()
    text = handler.get_text_from_image(ocr, cropped_image)
    num = find_numbers_in_string(text, "rude")

    # 如果小于 100，就说明没什么技能可以加了，点击【培育结束】
    if num < 100:
        d.click(520, 1080)
        time.sleep(DEFAULT_SLEEP_TIME)

    else:
        d.click(200, 1080)
        time.sleep(DEFAULT_SLEEP_TIME)

    """
        # 通过【技能Pt】的3个绿色，加上滚动条顶端的1个灰色，判断是否加技能界面
        if (
            np.all(screen[420, 300] == np.array([40, 211, 158]))
            and np.all(screen[420, 320] == np.array([40, 211, 158]))
            and np.all(screen[420, 440] == np.array([40, 211, 158]))
            and np.all(screen[420, 460] == np.array([40, 211, 158]))
        ):

            # 识别右上方【能力详情】按钮，再次 确认判断
            _image = cv2.imread(
                ROOT_DIR + "/resource/after_cultivate/find/skill_detail.png"
            )
            handler = ImageHandler()
            match = handler.is_sub_image_in_box(_image, screen, 600, 690, 300, 390)
            if match:
                print("page:::当前为加技能页面。")

                # 通过技能Pt数值来判断接下来的操作
                cropped_image = screen[406:436, 530:630]
                handler = ImageHandler()
                text = handler.get_text_from_image(ocr, cropped_image)
                num = find_numbers_in_string(text, "rude")
                if num < 100:
                    d.click(80, 1180)
                    time.sleep(DEFAULT_SLEEP_TIME)
                    continue
                # 否则，就开始加技能
                else:
                    add_skill = AddSkill(d, p_ocr, setting_dic)
                    add_skill.run()
        """
    """
        # 通过【培养结束确定】标题的2个绿色，加上【剩余技能Pt】的1个灰色，加上下方【警告icon】的红色，判断是否培育结束确认弹窗
        if (
            np.all(screen[320, 240] == np.array([10, 208, 134]))
            and np.all(screen[320, 480] == np.array([10, 208, 134]))
            and np.all(screen[760, 240] == np.array([229, 229, 237]))
            and np.all(screen[845, 210] == np.array([70, 105, 255]))
        ):
            # 识别上方【培养结束确定】标题，再次 确认判断
            _image = cv2.imread(
                ROOT_DIR + "/resource/cultivate/find/train_end_confirm.png"
            )
            handler = ImageHandler()
            match = handler.is_sub_image_in_box(_image, screen, 260, 460, 310, 350)
            if match:

                print("page:::当前为培育结束确认弹窗页面")
                d.click(520, 920)
                time.sleep(DEFAULT_SLEEP_TIME)
                break
        """


# test
if __name__ == "__main__":
    _d = u2.connect("127.0.0.1:16384")
    _ocr = ddddocr.DdddOcr()
    _p_ocr = PaddleOCR(use_angle_cls=True)
    _setting_dic = importlib.import_module("customer_setting.setting_1").data
    after_cultivate(_d, _ocr, _p_ocr, _setting_dic)

from method.recognition.imageMatcher import *
from method.recognition.textRecognizer import *
import uiautomator2 as u2
import ddddocr
import time
import numpy as np
from method.utils import *
import onnxruntime as ort


class Gift:
    def __init__(self, ocr: ddddocr.DdddOcr(), d: u2.connect()):
        self.ocr = ocr
        self.d = d
        self.resource_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/resource"

    def gift(self):

        while True:

            screen = self.d.screenshot(format="opencv")
            # 定义一下资源文件夹，后面会用到
            _dir = self.resource_dir + "/gift"

            # 如果都不是以上这些，则进入识图操作
            part_image_file_li = get_png_files(_dir + "/click")
            for part_image_file in part_image_file_li:
                part_image = cv2.imread(_dir + "/click/" + part_image_file)
                matcher = ImageMatcher(part_image, screen)
                match_result = matcher.find_part_image_from_total_image()
                if match_result is not None:
                    print(part_image_file)
                    point = match_result["result"]
                    self.d.click(point[0], point[1])
                    time.sleep(DEFAULT_SLEEP_TIME)
                    continue

            # 如果都不是以上这些，则进入识图操作
            part_image_file_li = get_png_files(self.resource_dir + "/general")
            for part_image_file in part_image_file_li:
                part_image = cv2.imread(self.resource_dir + "/general/" + part_image_file)
                matcher = ImageMatcher(part_image, screen, 0.7)
                match_result = matcher.find_part_image_from_total_image()
                if match_result is not None:
                    print(part_image_file)
                    point = match_result["result"]
                    self.d.click(point[0], point[1])
                    time.sleep(DEFAULT_SLEEP_TIME)
                    continue

            # x_li = [105, 275, 445, 615]
            """
            task_pink = screen[790, 690]  # 117, 50, 255
            gift_pink = screen[880, 690]

            if np.all(task_pink == np.array([117, 50, 255])) and np.all(gift_pink == np.array([117, 50, 255])):
                break
            """


if __name__ == "__main__":
    ort.set_default_logger_severity(3)
    d = u2.connect("127.0.0.1:16384")
    ocr = ddddocr.DdddOcr()
    gift = Gift(ocr, d)
    gift.gift()

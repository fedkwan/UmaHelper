from method.image_handler import *
from method.text_handler import *
import uiautomator2 as u2
import ddddocr
import time
from method.utils import *
import onnxruntime as ort


class Association:
    def __init__(self, ocr: ddddocr.DdddOcr(), d: u2.connect()):
        self.ocr = ocr
        self.d = d
        self.resource_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/resource"

    def association(self):

        give_status = 0
        request_status = 0

        _dir = self.resource_dir + "/association"

        # 进入社团首页
        while True:

            screen = self.d.screenshot(format="opencv")
            # 定义一下资源文件夹，后面会用到

            # 判断是否完成捐赠 后发先至
            if give_status != 1:
                part_image = cv2.imread(_dir + "/find/give_done.png")
                handler = ImageMatcher(part_image, screen)
                match_result = handler.find_part_image_from_total_image()
                if match_result:
                    give_status = 1
                    continue

            if give_status != 1:
                part_image = cv2.imread(_dir + "/find/shoes_give.png")
                handler = ImageMatcher(part_image, screen)
                match_result = handler.find_part_image_from_total_image()
                if match_result is not None:
                    point = match_result["result"]
                    self.d.click(point[0], point[1])
                    time.sleep(DEFAULT_SLEEP_TIME)
                    continue

            # 判断是否完成请求
            if request_status != 1:
                part_image = cv2.imread(_dir + "/find/request_title.png")
                handler = ImageMatcher(part_image, screen)
                match_result = handler.find_part_image_from_total_image()
                if match_result:
                    if np.all(screen[312, 620] == np.array([100, 100, 100])):
                        request_status = 1
                        continue

            if request_status != 1:
                part_image = cv2.imread(_dir + "/find/request_done.png")
                handler = ImageMatcher(part_image, screen)
                match_result = handler.find_part_image_from_total_image()
                if match_result is not None:
                    point = match_result["result"]
                    self.d.click(point[0], point[1])
                    time.sleep(DEFAULT_SLEEP_TIME)
                    continue

            # 如果都不是以上这些，则进入识图操作
            part_image_file_li = get_png_files(_dir + "/click")
            for part_image_file in part_image_file_li:
                part_image = cv2.imread(_dir + "/click/" + part_image_file)
                handler = ImageMatcher(part_image, screen)
                match_result = handler.find_part_image_from_total_image()
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
                handler = ImageMatcher(part_image, screen, 0.7)
                match_result = handler.find_part_image_from_total_image()
                if match_result is not None:
                    print(part_image_file)
                    point = match_result["result"]
                    self.d.click(point[0], point[1])
                    time.sleep(DEFAULT_SLEEP_TIME)
                    continue

            if give_status == 1 and request_status == 1:
                self.d.click(360, 1220)  # 回到首页
                time.sleep(DEFAULT_SLEEP_TIME)
                break


if __name__ == "__main__":
    ort.set_default_logger_severity(3)
    d = u2.connect("127.0.0.1:16384")
    ocr = ddddocr.DdddOcr()
    association = Association(ocr, d)
    association.association()

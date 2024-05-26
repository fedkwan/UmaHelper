from typing import Any

from airtest.aircv.template_matching import *
from paddleocr import PaddleOCR
import ddddocr
import numpy as np


class ImageHandler:

    @staticmethod
    def find_sub_image(small_image: np.array, big_image: np.array, threshold: float = 0.9) -> dict[str, Any] | None:
        # airtest 识图
        temp = TemplateMatching(small_image, big_image, threshold)
        best_match = temp.find_best_result()
        if best_match is not None:
            return best_match
        return None

    @staticmethod
    def is_sub_image_in_box(small_image: np.array, big_image: np.array, x0: int, x1: int, y0: int, y1: int, threshold: float = 0.9) -> bool:
        temp = TemplateMatching(small_image, big_image, threshold)
        best_match = temp.find_best_result()
        if best_match is not None:
            center = best_match['result']
            if x0 < center[0] < x1 and y0 < center[1] < y1:
                return True
        return False

    @staticmethod
    def get_text_from_image(ocr: PaddleOCR(), image: np.array) -> str:
        try:
            result = ocr.ocr(image)[0]
            _ = []
            for r in result:
                _.append(r[1][0])
            return "".join(_)
        except Exception as e:
            return str(e)

    @staticmethod
    def get_text_from_image_dddd(ocr: ddddocr.DdddOcr(), image: np.array) -> str:
        try:
            _, image_encode = cv2.imencode('.png', image)
            result = ocr.classification(image_encode.tobytes())
            return result
        except Exception as e:
            return str(e)

    # 计算两个颜色是否接近，请使用 B,G,R 顺序
    @staticmethod
    def count_color_diff(point_bgr_1: list, point_bgr_2: list, tolerance: int = 10) -> bool:
        distance = np.sqrt(np.sum((np.array(point_bgr_1) - np.array(point_bgr_2)) ** 2))
        print(distance)
        return distance < tolerance


# test
if __name__ == "__main__":
    _big_image = cv2.imread("temp/test_image.png")
    _small_image = _big_image[44:64, 15:150]  # y0,y1,x0,x1
    # cv2.imwrite("small_image.png", _small_image)

    _handler = ImageHandler()
    _ocr = PaddleOCR(use_angle_cls=True)
    _a = _handler.find_sub_image(_small_image, _big_image)
    _b = _handler.is_sub_image_in_box(_small_image, _big_image, 0, 200, 0, 100, 0.8)
    _c = _handler.get_text_from_image(_ocr, _small_image)

    print(_a)
    print(_b)
    print(_c)

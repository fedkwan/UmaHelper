from airtest.core.api import *
from airtest.aircv.aircv import *
from airtest.aircv.template_matching import *

import logging
import numpy as np

__author__ = "user"
logger = logging.getLogger("airtest")
logger.setLevel(logging.ERROR)
auto_setup(__file__)


# 请传入 cv2.imread 读取的对象，使用 png 格式
class ImageMatcher:
    def __init__(self, part_image, total_image, threshold=0.9):
        self.part_image = part_image
        self.total_image = total_image
        self.threshold = threshold

    # 计算两个颜色是否接近，请使用 B,G,R 顺序
    @staticmethod
    def count_color_diff(point_bgr_1: list, point_bgr_2: list, tolerance: int = 10) -> bool:
        distance = np.sqrt(np.sum((np.array(point_bgr_1) - np.array(point_bgr_2)) ** 2))
        print(distance)
        return distance < tolerance

    def find_part_image_from_total_image(self):
        temp = TemplateMatching(self.part_image, self.total_image, self.threshold)
        best_match = temp.find_best_result()
        if best_match is not None:
            return best_match
        return None

    def is_part_image_in_box(self, x0, x1, y0, y1) -> bool:
        temp = TemplateMatching(self.part_image, self.total_image, self.threshold)
        best_match = temp.find_best_result()
        if best_match is not None:
            center = best_match['result']
            if x0 < center[0] < x1 and y0 < center[1] < y1:
                return True
        return False

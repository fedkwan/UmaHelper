import time
import cv2
import uiautomator2 as u2
from method.recognition.textRecognizer import *
import ddddocr
import onnxruntime as ort
from method.recognition.imageMatcher import *

ort.set_default_logger_severity(3)
ocr = ddddocr.DdddOcr()

d = u2.connect("127.0.0.1:16384")
screen = d.screenshot(format="opencv")

part_image = cv2.imread("resource/association/condition/give_done.png")

matcher = ImageMatcher(part_image, screen)
mt = matcher.find_part_image_from_total_image()
print(mt)

"""
file_name_li = "210,930-210,300,832,972.png"[0:-4].split("-")
[click_x, click_y] = list(map(int, file_name_li[0].split(",")))
[x0, x1, y0, y1] = list(map(int, file_name_li[1].split(",")))
matcher = ImageMatcher(part_image, screen)
mt = matcher.find_part_image_from_total_image()
print(mt)
match_result = matcher.is_part_image_in_box(x0 - 20, x1 + 20, y0 - 20, y1 + 20)
print(match_result)
"""

"""
temp = TemplateMatching(part_image, screen)
setattr(temp, 'threshold', 0.9)
best_match = temp.find_best_result()
if best_match is not None:
    center = best_match['result']
    print(center)
    d.click(center[0], center[1])
"""
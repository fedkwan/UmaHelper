import uiautomator2 as u2
import onnxruntime as ort
from method.image_handler import *

ort.set_default_logger_severity(3)
ocr = PaddleOCR()

d = u2.connect("127.0.0.1:16384")
screen = d.screenshot(format="opencv")

# part_image = cv2.imread("resource/association/condition/give_done.png")

# matcher = ImageMatcher(part_image, screen)
# mt = matcher.find_part_image_from_total_image()
# print(mt)

cropped_image = screen[11:37, 610:690]

matcher = ImageHandler()
text = matcher.get_text_from_image(ocr, cropped_image)

print(text)

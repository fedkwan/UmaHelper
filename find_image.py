import uiautomator2 as u2

from method.image_handler import *

from setting.base import *

ort.set_default_logger_severity(3)
ocr = ddddocr.DdddOcr()
p_ocr = PaddleOCR()

d = u2.connect("127.0.0.1:16384")
screen = d.screenshot(format="opencv")

_image = cv2.imread(ROOT_DIR + "/resource/before_cultivate/click/start_cultivate.png")
handler = ImageHandler()
match = handler.find_sub_image(_image, screen)
if match:
    print(match)
"""
cropped_image = screen[11:37, 610:690]

matcher = ImageHandler()
text = matcher.get_text_from_image(ocr, cropped_image)

cropped_image = screen[406:436, 530:630]
handler = ImageHandler()
text = handler.get_text_from_image(ocr, cropped_image)
num = find_numbers_in_string(text, "rude")

print(text)
print(num)
"""

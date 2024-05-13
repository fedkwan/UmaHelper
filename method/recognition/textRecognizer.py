import cv2


# 请传入 cv2.imread 读取的对象，使用 png 格式
class TextRecognizer:

    def __init__(self, image, ocr):
        self.image = image
        self.ocr = ocr

    def find_text_from_image(self):
        _, image_encode = cv2.imencode('.png', self.image)
        str_match = self.ocr.classification(image_encode.tobytes())
        return str_match

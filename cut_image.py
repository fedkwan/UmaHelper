import time
import cv2
import uiautomator2 as u2
from method.recognition.textRecognizer import *
import ddddocr
import onnxruntime as ort

ort.set_default_logger_severity(3)
# ocr = ddddocr.DdddOcr()

d = u2.connect("127.0.0.1:16384")
screen = d.screenshot(format="opencv")
# screen = cv2.imread("x.png")


print(screen.shape)
cropped_image = screen[266:326, 45:130]
cv2.imwrite("cut" + str(time.time()) + ".png", cropped_image)
cropped_image = screen[441:501, 45:130]
cv2.imwrite("cut" + str(time.time()) + ".png", cropped_image)
cropped_image = screen[616:676, 45:130]
cv2.imwrite("cut" + str(time.time()) + ".png", cropped_image)
cropped_image = screen[791:851, 45:130]
cv2.imwrite("cut" + str(time.time()) + ".png", cropped_image)
cropped_image = screen[966:1026, 45:130]
cv2.imwrite("cut" + str(time.time()) + ".png", cropped_image)
# text_recognizer = TextRecognizer(cropped_image, ocr)
# x = text_recognizer.find_text_from_image()
# print(x)

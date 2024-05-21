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
cropped_image = screen[677:757, 50:130]
cv2.imwrite("cut" + str(time.time()) + ".png", cropped_image)
cropped_image = screen[677:757, 185:265]
cv2.imwrite("cut" + str(time.time()) + ".png", cropped_image)
cropped_image = screen[677:757, 320:400]
cv2.imwrite("cut" + str(time.time()) + ".png", cropped_image)
cropped_image = screen[677:757, 455:535]
cv2.imwrite("cut" + str(time.time()) + ".png", cropped_image)
cropped_image = screen[677:757, 590:670]
cv2.imwrite("cut" + str(time.time()) + ".png", cropped_image)
# text_recognizer = TextRecognizer(cropped_image, ocr)
# x = text_recognizer.find_text_from_image()
# print(x)

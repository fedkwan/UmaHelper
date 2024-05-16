import time
import numpy as np
import importlib
import re
from method.recognition.textRecognizer import *
from module.cultivate.get_attribute import *
from module.cultivate.get_attribute_up_if_train import *


class Train:
    def __init__(self, ocr, d, uma_name):
        self.ocr = ocr
        self.d = d
        self.uma_name = uma_name

    @staticmethod
    def get_train_index(self, train_type_text) -> int:
        if "速度" in train_type_text:
            return 0
        elif "持久" in train_type_text:
            return 1
        elif "力量" in train_type_text:
            return 2
        elif "意志" in train_type_text:
            return 3
        else:
            return 4

    def train(self):

        screen = self.d.screenshot(format="opencv")

        # 获取当前五维
        attribute_result_li = get_attribute(screen, self.ocr)

        uma_name = "resource.uma_file" + "." + self.uma_name
        uma_model = importlib.import_module(uma_name)
        train_target = uma_model.data["train_target"]

        np_train_gap_li = np.subtract(np.array(attribute_result_li), np.array(train_target))
        print(np_train_gap_li)

        if np.any(np_train_gap_li < 0):
            train_selection_li = np.where(np_train_gap_li < 0)[0].tolist()
        else:
            train_selection_li = [0, 1, 2, 3, 4]

        print(train_selection_li)

        cropped_image = screen[207:229, 99:204]
        text_recognizer = TextRecognizer(cropped_image, self.ocr)
        train_type_text = text_recognizer.find_text_from_image()

        train_index = self.get_train_index(self, train_type_text)
        print(train_index)

        result_li = []
        chose_selection_dictionary = {}
        cli = []

        if train_index in train_selection_li:
            result_li = get_attribute_up_if_train(screen, self.ocr, train_index)
            chose_selection_dictionary[100 + train_index * 130] = sum(result_li)
            train_selection_li.remove(train_index)

        print(train_selection_li)
        for selection in train_selection_li:
            x = 100 + selection * 130
            self.d.click(x, 1080)
            time.sleep(0.3)
            screen_image2 = self.d.screenshot(format="opencv")

            result_li = get_attribute_up_if_train(screen_image2, self.ocr, selection)
            chose_selection_dictionary[x] = sum(result_li)

        print(chose_selection_dictionary)

        max_value_key = max(chose_selection_dictionary, key=chose_selection_dictionary.get)
        self.d.click(max_value_key, 1080)
        time.sleep(0.5)
        self.d.click(max_value_key, 1080)
        time.sleep(2)

    def get_pt(self, screen):
        cropped_image = screen[854:905, 599:695]
        text_recognizer = TextRecognizer(cropped_image, self.ocr)
        result_num = text_recognizer.find_text_from_image()
        return result_num

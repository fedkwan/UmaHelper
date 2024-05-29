import importlib

import uiautomator2 as u2

from setting.base import *
from module.cultivate.get_attribute import *
from module.cultivate.get_attribute_up_if_train import *

train_index_dic = {
    "速度": 0, "持久": 1, "力量": 2, "意志": 3, "智力": 4
}


def train(d: u2.connect, ocr: ddddocr.DdddOcr, p_ocr: PaddleOCR, setting_dic: dict):
    screen = d.screenshot(format="opencv")

    # 获取当前五维
    attribute_li = get_attribute(ocr, screen)
    print(attribute_li)
    train_target = setting_dic["train_target"]
    np_train_gap_li = np.subtract(np.array(attribute_li), np.array(train_target))
    print(np_train_gap_li)

    # 计算与培育目标的差值
    if np.any(np_train_gap_li < 0):
        train_selection_li = np.where(np_train_gap_li < 0)[0].tolist()
    else:
        train_selection_li = [0, 1, 2, 3, 4]
    print(train_selection_li)

    # 获取当前在哪个训练分类
    cropped_image = screen[207:229, 99:204]
    handler = ImageHandler()
    train_type_text = handler.get_text_from_image(ocr, cropped_image)[0:2]
    print(train_type_text)
    if " " not in train_type_text:
    # train_index = get_train_index(self, train_type_text)
        train_index = train_index_dic[train_type_text]
    else:
        train_index = 0
    print(train_index)

    chose_selection_dicionary = {}
    # 如果点进去这个正好是需要训练的，那就先看
    if train_index in train_selection_li:
        result_li = get_attribute_up_if_train(screen, ocr, train_index)
        chose_selection_dicionary[100 + train_index * 130] = sum(result_li)
        train_selection_li.remove(train_index)
    print(train_selection_li)

    # 然后再看其他的
    for selection in train_selection_li:
        x = 100 + selection * 130
        d.click(x, 1080)
        time.sleep(0.3)
        _screen_image = d.screenshot(format="opencv")
        result_li = get_attribute_up_if_train(_screen_image, ocr, selection)
        chose_selection_dicionary[x] = sum(result_li)
    print(chose_selection_dicionary)

    # 选出最终需要训练的
    max_value_key = max(chose_selection_dicionary, key=chose_selection_dicionary.get)
    d.click(max_value_key, 1080)
    time.sleep(DEFAULT_SLEEP_TIME)
    d.click(max_value_key, 1080)
    time.sleep(DEFAULT_SLEEP_TIME * 4)


# test
if __name__ == "__main__":
    _d = u2.connect("127.0.0.1:16384")
    _ocr = ddddocr.DdddOcr()
    _p_ocr = PaddleOCR(use_angle_cls=True)
    _setting_dic = importlib.import_module("customer_setting.setting_1").data
    train(_d, _ocr, _p_ocr, _setting_dic)

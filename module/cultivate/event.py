from paddleocr import PaddleOCR
import numpy as np
from method.image_handler import *
from module.cultivate.get_round import *


def event(d: u2.connect, screen: np.array, p_ocr: PaddleOCR, setting_dic: dict):

    if np.all(screen[679, 360] == np.array([3, 206, 121])):
        if setting_dic["target_scenario"] == "youth":
            this_round = get_round(screen, p_ocr, setting_dic["target_scenario"])
            if this_round == 1:
                d.click(360, 830)
            else:
                d.click(360, 720)
        else:
            d.click(360, 720)
    elif np.all(screen[567, 360] == np.array([3, 206, 121])):
        d.click(360, 610)
    elif np.all(screen[343, 360] == np.array([3, 206, 121])):
        d.click(360, 830)

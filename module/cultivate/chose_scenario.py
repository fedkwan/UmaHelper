import uiautomator2 as u2
import importlib
import time
import numpy as np
from method.utils import *


def chose_scenario(d: u2.connect(), setting_file_name):
    setting_data = importlib.import_module("customer_setting" + "." + setting_file_name).data
    target_scenario = setting_data["target_scenario"]
    scenario_to_x_dic = {
        "ura": 316,
        "youth": 345,
        "peak": 375,
        "idol": 404
    }

    while True:
        screen = d.screenshot(format="opencv")
        if np.all(screen[1016, scenario_to_x_dic[target_scenario]] == np.array([24, 222, 156])):
            d.click(360, 1080)
            break
        d.click(30, 585)
        time.sleep(DEFAULT_SLEEP_TIME)
        continue


# test
if __name__ == "__main__":
    _d = u2.connect("127.0.0.1:16384")
    chose_scenario(_d, "setting_1")

import uiautomator2 as u2
import importlib
import time

from setting.base import *
from method.utils import *


def chose_scenario(d: u2.connect, setting_dic: dict):
    target_scenario = setting_dic["target_scenario"]
    scenario_to_x_dic = {
        "ura": 300,
        "youth": 330,
        "peak": 359,
        "idol": 388,
        "master": 418
    }

    while True:
        screen = d.screenshot(format="opencv")
        if np.all(screen[1016, scenario_to_x_dic[target_scenario]] == np.array([24, 222, 156])):
            break
        d.click(30, 585)
        time.sleep(DEFAULT_SLEEP_TIME)
        continue


# test
if __name__ == "__main__":
    _d = u2.connect("127.0.0.1:16384")
    _setting_dic = importlib.import_module("customer_setting.setting_1").data
    chose_scenario(_d, _setting_dic)

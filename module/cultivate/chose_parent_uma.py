import uiautomator2 as u2
import importlib
import time
import numpy as np
from method.utils import *


def chose_parent_uma(d: u2.connect(), setting_file_name):
    d.swipe(360, 900, 360, 610, 1)


# test
if __name__ == "__main__":
    _d = u2.connect("127.0.0.1:16384")
    chose_parent_uma(_d, "setting_1")

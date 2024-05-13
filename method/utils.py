import os
import datetime

DEFAULT_SLEEP_TIME = 0.5


def get_png_files(folder):
    png_files = []
    files = os.listdir(folder)
    for file in files:
        if file.endswith(".png"):
            png_files.append(file)
    return png_files


def is_monday_midnight_to_five():
    # 获取当前时间
    current_time = datetime.datetime.now()

    # 判断当前时间是否是周一并且时间在 0 点到 6 点之间
    if current_time.weekday() == 0 and current_time.hour < 5:
        return True
    else:
        return False

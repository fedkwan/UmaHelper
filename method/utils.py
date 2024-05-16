import os
import datetime

DEFAULT_SLEEP_TIME = 0.5


def find_numbers_in_string(string, model="stable"):
    numbers = re.findall(r'\d+', string)
    if not numbers:
        if model == "stable":
            return None
        elif model == "rude":
            return 0
    return int(''.join(numbers))


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

import os
import re
import datetime
import numpy as np

DEFAULT_SLEEP_TIME = 0.5
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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


# 将一个数组里面，相邻的两个数差不超过2的归类到一个新子组里，最后输出统计的各子组的中位数
def merge_close_values(arr):
    # 如果输入数组为空，返回空数组
    if not arr:
        return []
    # 初始化结果数组和当前子数组
    result = []
    current_subarray = [arr[0]]
    for i in range(1, len(arr)):
        # 如果当前值和前一个值的差小于2，加入当前子数组
        if arr[i] - arr[i - 1] < 2:
            current_subarray.append(arr[i])
        else:
            # 否则，将当前子数组加入结果数组并开始新的子数组
            result.append(int(np.median(current_subarray)))
            current_subarray = [arr[i]]
    # 将最后一个子数组加入结果数组
    result.append(int(np.median(current_subarray)))
    return result


# test
if __name__ == "__main__":
    print(root_dir)

import importlib

import uiautomator2 as u2

from setting.base import *
from method.image_handler import *


def chose_parent_uma(d: u2.connect, setting_dic: dict):
    uma_rank_1 = setting_dic["parent_uma_rank_1"]
    uma_rank_2 = setting_dic["parent_uma_rank_2"]
    uma_rank_friend = setting_dic["parent_uma_rank_friend"]

    while True:
        screen = d.screenshot(format="opencv")

        # 第1位 隔壁的蓝色来判断，是准备进入选种马阶段
        if np.all(screen[660, 110] == np.array([247, 179, 36])):

            # 如果没有【遗传树】的灰色，左边没有就点左边
            if np.all(screen[775, 215] != np.array([196, 196, 196])):
                d.click(110, 800)
                time.sleep(DEFAULT_SLEEP_TIME)

            # 如果没有【遗传树】的灰色，右边没有就点右边
            elif np.all(screen[775, 555] != np.array([196, 196, 196])):
                d.click(450, 800)
                time.sleep(DEFAULT_SLEEP_TIME)

            # 两边都选好了，就点下一步
            else:
                break

        # 选马娘里面，蓝色边框就是第1位
        if np.all(screen[690, 360] == np.array([245, 194, 87])):
            scroll_to_chose_parent_uma(d, uma_rank_1)

        # 选马娘里面，粉色边框就是第2位
        if np.all(screen[690, 360] == np.array([193, 142, 251])):

            # 如果租借右上角的还剩X次的粉色还存在，就借好友的（没钱别怪我）
            if np.all(screen[635, 700] == np.array([117, 50, 255])):
                d.click(530, 655)
                time.sleep(DEFAULT_SLEEP_TIME)
                scroll_to_chose_parent_uma(d, uma_rank_friend)

            # 否则就选自己的吧
            else:
                scroll_to_chose_parent_uma(d, uma_rank_2)

        time.sleep(DEFAULT_SLEEP_TIME)

        # 这里统一处理一下吧，不想放到外面的循环去处理，显得比较整洁
        sub_image = cv2.imread(ROOT_DIR + "/resource/general/ok.png")
        handler = ImageHandler()
        best_match = handler.find_sub_image(sub_image, screen)
        if best_match is not None:
            click_x, click_y = best_match["result"]
            d.click(click_x, click_y)
            time.sleep(DEFAULT_SLEEP_TIME)


def scroll_to_chose_parent_uma(d: u2.connect, rank: int):
    rank = rank - 1
    count = 0
    while True:
        screen = d.screenshot(format="opencv")
        li = []
        for y in range(691, 972):
            # 特意选的一个X值，在第四列马娘的左侧一点点，用于区分每行的区间，空白的地方rgb加起来一般会大于720
            rgb_sum = np.sum(screen[y, 427])
            if rgb_sum < 720:
                li.append(y)

        merged_array = merge_close_values(li)

        x_li = [90, 225, 360, 495, 630, 90, 225, 360, 495, 630]
        if int(rank / 10) == count:
            p = rank % 10
            if p < 5:
                d.click(x_li[p], merged_array[0])
                time.sleep(DEFAULT_SLEEP_TIME)
                d.click(360, 1080)
            elif p >= 5:
                d.click(x_li[p], merged_array[1])
                time.sleep(DEFAULT_SLEEP_TIME)
                d.click(360, 1080)
            break

        d.swipe(360, 900, 360, 600, 1)
        count = count + 1
        time.sleep(DEFAULT_SLEEP_TIME)


# 将一个数组里面，相邻的两个数差不超过2的归类到一个新子组里，最后输出统计的各子组的中位数
def merge_close_values(arr):
    if not arr:
        return []
    result = []
    current_subarray = [arr[0]]
    for i in range(1, len(arr)):
        if arr[i] - arr[i - 1] < 2:
            current_subarray.append(arr[i])
        else:
            result.append(int(np.median(current_subarray)))
            current_subarray = [arr[i]]
    result.append(int(np.median(current_subarray)))
    return result


# test
if __name__ == "__main__":
    _d = u2.connect("127.0.0.1:16384")
    _setting_dic = importlib.import_module("customer_setting.setting_1").data
    chose_parent_uma(_d, _setting_dic)

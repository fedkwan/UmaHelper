import re
from method.recognition.textRecognizer import *


def find_numbers_in_string(string, model="stable"):
    numbers = re.findall(r'\d+', string)
    if not numbers:
        if model == "stable":
            return None
        elif model == "rude":
            return 0
    return int(''.join(numbers))


def get_round(screen, ocr):

    cropped_image = screen[44:64, 15:150]
    text_recognizer = TextRecognizer(cropped_image, ocr)
    stage_str = text_recognizer.find_text_from_image().replace("-", "").replace("了", "7")  # 这里是会把 7 识别为 了，只能等 dddd 作者优化了
    # cv2.imwrite("round_title.png", cropped_image)
    # print(stage_str)

    result_num, year, month, half = 99, 99, 99, 99
    if "手" in stage_str:
        year = 0
        if "出" in stage_str:
            rookie_calendar_dict = {
                11: (0, 0), 10: (0, 1), 9: (1, 0), 8: (1, 1), 7: (2, 0), 6: (2, 1),
                5: (3, 0), 4: (3, 1), 3: (4, 0), 2: (4, 1), 1: (5, 0), -1: (99, 99)
            }
            cropped_image2 = screen[98:154, 11:141]
            text_recognizer2 = TextRecognizer(cropped_image2, ocr)
            round_until_target_str = text_recognizer2.find_text_from_image()
            round_until_target_num = find_numbers_in_string(round_until_target_str)
            month, half = rookie_calendar_dict[round_until_target_num]
        else:
            month = find_numbers_in_string(stage_str) - 1
            half = 0 if "前" in stage_str else 1
    elif "典" in stage_str:
        year = 1
        month = find_numbers_in_string(stage_str) - 1
        half = 0 if "前" in stage_str else 1
    elif "深" in stage_str:
        year = 2
        month = find_numbers_in_string(stage_str) - 1
        half = 0 if "前" in stage_str else 1

    # print(str(year) + ":" + str(month) + ":" + str(half))

    result_num = 2 * (12 * year + month) + half + 1
    return result_num

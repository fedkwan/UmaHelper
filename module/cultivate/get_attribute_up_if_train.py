from method.recognition.textRecognizer import *
from method.utils import *


def train_selection_split(arr, index):
    if index == 0:
        return [arr[0], arr[2]]
    elif index == 1:
        return [arr[1], arr[3]]
    elif index == 2:
        return [arr[1], arr[2]]
    elif index == 3:
        return [arr[0], arr[2], arr[3]]
    elif index == 4:
        return [arr[0], arr[4]]
    else:
        return "Invalid index"


def is_first_col_contain_orange(image):
    orange = [(157, 225, 252), (143, 237, 255), (140, 237, 255), (138, 237, 255), (141, 238, 255), (139, 236, 255), (132, 234, 255),
              (121, 230, 255),
              (112, 227, 255), (110, 223, 255), (110, 220, 255), (110, 217, 255), (112, 214, 255), (114, 210, 255), (116, 205, 255),
              (112, 197, 255),
              (105, 187, 255), (91, 177, 255), (85, 169, 255), (79, 162, 255), (77, 156, 255), (75, 149, 255), (74, 141, 255), (74, 132, 255),
              (74, 123, 255), (77, 111, 254), (87, 120, 251), (115, 148, 255), (157, 225, 251), (153, 221, 255), (138, 239, 255),
              (135, 238, 255),
              (130, 237, 255), (116, 228, 255), (109, 224, 255), (103, 220, 254), (107, 217, 255), (110, 212, 255), (113, 207, 255),
              (112, 199, 255),
              (102, 187, 255), (93, 175, 255), (78, 162, 255), (73, 155, 255), (69, 148, 255), (76, 134, 251), (76, 128, 251), (76, 125, 251),
              (91, 125, 244), (113, 147, 255), (147, 215, 253), (139, 241, 255), (136, 238, 255), (136, 238, 255), (155, 230, 255),
              (94, 161, 225),
              (26, 91, 193), (111, 158, 217), (66, 97, 193), (42, 73, 178), (88, 138, 220), (125, 206, 255), (119, 202, 255), (113, 197, 255),
              (102, 187, 255), (101, 186, 255), (108, 125, 213), (40, 58, 176), (37, 55, 173), (31, 51, 167), (81, 132, 229), (90, 141, 255),
              (76, 121, 251), (73, 113, 253), (93, 127, 246), (117, 151, 255)]

    shape = image.shape
    oran = 0
    for row in range(shape[0]):
        (b, g, r) = image[row, 0]
        bgr = (b, g, r)
        if bgr in orange:
            oran = oran + 1
    if oran >= 5:
        return True
    else:
        return False


def get_attribute_up_if_train(screen, ocr, selection):
    x_base_li = [82, 196, 309, 421, 534]
    result_li = [0 for _ in range(3 if selection == 3 else 2)]  # 创建空数组
    x_single_selection_li = train_selection_split([[i, i + 30] for i in x_base_li], selection)  # 先对一位数宽度截图一次
    x_double_selection_li = train_selection_split([[i - 14, i + 46] for i in x_base_li], selection)  # 再对两位数宽度截图一次

    result_single, result_double = [], []
    s, d = 0, 0

    for x_pair in x_single_selection_li:
        cropped_image = screen[780:820, x_pair[0]:x_pair[1]]
        text_recognizer = TextRecognizer(cropped_image, ocr)
        attribute_up_number = text_recognizer.find_text_from_image()
        if is_first_col_contain_orange(cropped_image):
            result_single.append("")
        else:
            result_single.append(attribute_up_number)
        s = s + 1
        cv2.imwrite("temp/single" + str(s) + ".png", cropped_image)

    for x_pair in x_double_selection_li:
        cropped_image = screen[780:820, x_pair[0]:x_pair[1]]
        text_recognizer = TextRecognizer(cropped_image, ocr)
        attribute_up_number = text_recognizer.find_text_from_image()
        if is_first_col_contain_orange(cropped_image):
            result_double.append("")
        else:
            result_double.append(attribute_up_number)
        d = d + 1
        cv2.imwrite("temp/double" + str(d) + ".png", cropped_image)

    for i in range(0, len(result_li)):
        if result_single[i] != "" and result_double[i] != "":
            result_li[i] = find_numbers_in_string(result_single[i], "rude") + find_numbers_in_string(result_double[i], "rude")
        if result_single[i] != "" and result_double[i] == "":
            result_li[i] = find_numbers_in_string(result_single[i], "rude")
        if result_single[i] == "" and result_double[i] != "":
            result_li[i] = find_numbers_in_string(result_double[i], "rude")
    return result_li


# test
if __name__ == "__main__":
    # _d = u2.connect("127.0.0.1:16384")
    # _screen = _d.screenshot(format="opencv")
    import cv2
    import uiautomator2 as u2


    _screen = cv2.imread("../../temp.png")
    _ocr = ddddocr.DdddOcr()
    print(get_attribute(_screen, _ocr))
    print(type(_screen))
from method.recognition.imageMatcher import *
from method.recognition.textRecognizer import *


def get_power(self):
    screen = d.screenshot(format="opencv")

    cropped_image = screen[161:162, 227:517]
    shape = cropped_image.shape
    i = 0
    for col in range(shape[1]):
        (b, g, r) = cropped_image[0, col]
        if (b, g, r) != (117, 117, 117):
            i = i + 1
        else:
            break
    result_num = round(i / 290 * 100)
    # cv2.imwrite("power.png", cropped_image)
    return result_num


def get_mood(self):
    screen = d.screenshot(format="opencv")
    """
    cropped_image = screen[147:176, 578:635]
    text_recognizer = TextRecognizer(cropped_image, ocr)
    result_str = text_recognizer.find_text_from_image()
    # cv2.imwrite("mood.png", cropped_image)
    return result_str
    """
    (b, g, r) = screen[140, 590]
    mood_list = [(105, 20, 241), (17, 90, 240), (3, 139, 207), (241, 105, 37), (206, 52, 140)]
    for i in range(0, 5):
        if (b, g, r) == mood_list[i]:
            return i
    return 99


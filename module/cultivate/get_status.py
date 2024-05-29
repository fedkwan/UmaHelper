import uiautomator2 as u2

from setting.base import *
from method.image_handler import *

logging.getLogger("airtest").setLevel(logging.ERROR)


def get_status(screen: np.array) -> dict:
    # 获取当前回合数、体力、心情、五维数值
    result = {
        "power": 100,  # 默认 100
        "mood": 2,  # 红、橙、黄、蓝、紫
    }

    # power
    cropped_image = screen[161:162, 227:517]
    for col in range(0, 290):
        if np.all(cropped_image[0, col] == np.array([117, 117, 117])):
            result["power"] = round(col / 290 * 100)
            break

    # mood
    mood_list = [[105, 20, 241], [17, 90, 240], [3, 139, 207], [241, 105, 37], [206, 52, 140]]
    pixel_color = screen[140, 590].tolist()
    result["mood"] = mood_list.index(pixel_color) if pixel_color in mood_list else 5

    return result


# test
if __name__ == "__main__":
    _d = u2.connect("127.0.0.1:16384")
    _result = get_status(_d)
    print(_result)

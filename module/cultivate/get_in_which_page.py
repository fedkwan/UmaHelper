from method.recognition.imageMatcher import *
from method.recognition.textRecognizer import *


def in_which_page(screen, ocr, _dir):
    # 如果是【游戏登录后】的首页
    # 点进培育
    if np.all(screen[1261, 360] == np.array([247, 159, 28])):
        return "app_main"

    # 根据技能图标 判断 当前是不是培育主界面
    skill_prat_image = cv2.imread(_dir + "/find/skill.png")
    image_matcher = ImageMatcher(skill_prat_image, screen)
    skill_match = image_matcher.is_part_image_in_box(540, 660, 940, 1040)
    if skill_match:
        return "main"
        # 根据状态，判断要做什么

    # 根据左上角的文字 判断 当前是不是训练界面
    cropped_image = screen[207:229, 101:141]
    text_recognizer = TextRecognizer(cropped_image, ocr)
    train_type_str = text_recognizer.find_text_from_image()
    train_type_li = ["速度", "持久", "力量", "意志", "智力"]
    if train_type_str in train_type_li:
        return "train"
        # 执行轮询，然后训练即可

    # 根据是否有行程表的文字 或者 是否出现了左或右标志 判断 当前是不是竞赛界面
    """
    competition_cropped_image = screen[1065:1095, 540:660]
    competition_text_recognizer = TextRecognizer(competition_cropped_image, ocr)
    competition_schedule_str = competition_text_recognizer.find_text_from_image()
    print(competition_schedule_str)
    term1 = "行程表" in competition_schedule_str
    """
    competition_prev_image = cv2.imread(_dir + "/find/competition_prev.png")
    competition_next_image = cv2.imread(_dir + "/find/competition_next.png")
    competition_prev_image_matcher = ImageMatcher(competition_prev_image, screen)
    competition_next_image_matcher = ImageMatcher(competition_next_image, screen)
    competition_prev_match = competition_prev_image_matcher.is_part_image_in_box(70, 160, 600, 690)
    competition_next_match = competition_next_image_matcher.is_part_image_in_box(560, 650, 600, 690)

    cropped_image = screen[920:943, 220:460]
    # cv2.imwrite("cut" + str(time.time()) + ".png", cropped_image)
    text_recognizer = TextRecognizer(cropped_image, ocr)
    x = text_recognizer.find_text_from_image()

    if competition_prev_match or competition_next_match:
        if "以外的" in x:
            return "competition_set_select"
        else:
            return "competition"
            # 应该是一步步点击

    # 根据左上角的title和右下角的重置 判断 当前是否加技能界面
    skill_title_cropped_image = screen[10:34, 20:120]
    # cv2.imwrite("cut" + str(time.time()) + ".png", skill_title_cropped_image)
    skill_title_text_recognizer = TextRecognizer(skill_title_cropped_image, ocr)
    skill_title_text = skill_title_text_recognizer.find_text_from_image()

    skill_reset_cropped_image = screen[1065:1095, 560:680]
    # cv2.imwrite("cut" + str(time.time()) + ".png", skill_reset_cropped_image)
    skill_reset_text_recognizer = TextRecognizer(skill_reset_cropped_image, ocr)
    skill_reset_text = skill_reset_text_recognizer.find_text_from_image()
    if ("技能" in skill_title_text) and (skill_reset_text == "重置"):
        return "skill"

    # 根据是否出现两个选项马蹄铁图片 判断 当前是否事件界面
    event_green_image = cv2.imread(_dir + "/find/event_green.png")
    event_yellow_image = cv2.imread(_dir + "/find/event_yellow.png")
    event_green_image_matcher = ImageMatcher(event_green_image, screen)
    event_yellow_image_matcher = ImageMatcher(event_yellow_image, screen)
    event_green_match = event_green_image_matcher.is_part_image_in_box(30, 70, 0, 1280)
    event_yellow_match = event_yellow_image_matcher.is_part_image_in_box(30, 70, 0, 1280)
    if event_green_match and event_yellow_match:
        return "event"

    inherit_cropped_image = screen[1028:1075, 266:345]
    inherit_text_recognizer = TextRecognizer(inherit_cropped_image, ocr)
    inherit_text = inherit_text_recognizer.find_text_from_image()
    if inherit_text == "因子":
        return "inherit"

    cropped_image = screen[1040:1075, 310:410]
    # cv2.imwrite("cut" + str(time.time()) + ".png", cropped_image)
    text_recognizer = TextRecognizer(cropped_image, ocr)
    k = text_recognizer.find_text_from_image()
    if k == "tap":
        return "competition_result"

    fans_require_image = cv2.imread(_dir + "/find/fans_require.png")
    fans_require_image_matcher = ImageMatcher(fans_require_image, screen)
    fans_require_match = fans_require_image_matcher.is_part_image_in_box(247, 476, 310, 350)
    if fans_require_match:
        return "fans_require"

    fans_require_image = cv2.imread(_dir + "/find/target_times_require.png")
    fans_require_image_matcher = ImageMatcher(fans_require_image, screen)
    fans_require_match = fans_require_image_matcher.is_part_image_in_box(230, 492, 310, 350)
    if fans_require_match:
        return "target_times_require"

    fans_require_image = cv2.imread(_dir + "/find/consecutive_competition.png")
    fans_require_image_matcher = ImageMatcher(fans_require_image, screen)
    fans_require_match = fans_require_image_matcher.is_part_image_in_box(292, 428, 393, 434)
    if fans_require_match:
        return "consecutive_competition"

    fans_require_image = cv2.imread(_dir + "/find/target_competition_fans_require.png")
    fans_require_image_matcher = ImageMatcher(fans_require_image, screen)
    fans_require_match = fans_require_image_matcher.is_part_image_in_box(215, 508, 309, 350)
    if fans_require_match:
        return "target_competition_fans_require"

    fans_require_image = cv2.imread(_dir + "/find/toy_grab.png")
    fans_require_image_matcher = ImageMatcher(fans_require_image, screen, 0.8)
    fans_require_match = fans_require_image_matcher.find_part_image_from_total_image()
    if fans_require_match:
        return "toy_grab"

    fans_require_image = cv2.imread(_dir + "/find/toy_grab_ok.png")
    fans_require_image_matcher = ImageMatcher(fans_require_image, screen)
    fans_require_match = fans_require_image_matcher.is_part_image_in_box(333, 386, 1168, 1202)
    if fans_require_match:
        return "toy_grab_ok"


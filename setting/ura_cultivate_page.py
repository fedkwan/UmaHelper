ura_cultivate_page_data = {
    "app_main": {
        "points": {
            (1264, 300): [220, 130, 0],  # y,x : b, g, r
            (1264, 330): [220, 130, 0],
            (1264, 360): [220, 130, 0],
            (920, 650): [102, 68, 221],
        },
        "sub_image_position": [220, 270, 1090, 1110],  # x0, x1, y0, y1
        "expect_page_list": ["chose_scenario"],
    },
    "chose_scenario": {
        "points": {
            (222, 500): [101, 54, 247],
            (222, 520): [101, 54, 247],
            (222, 630): [101, 54, 247],
            (222, 650): [101, 54, 247],
        },
        "sub_image_position": [527, 620, 127, 157],
        "expect_page_list": ["chose_uma"],
    },
    "chose_uma": {
        "points": {
            (460, 150): [36, 217, 121],
            (460, 410): [36, 217, 121],
            (460, 670): [36, 217, 121],
            (367, 64): [29, 209, 255],
        },
        "sub_image_position": [470, 563, 402, 432],
        "expect_page_list": ["chose_parent_uma"],
    },
    "chose_parent_uma": {
        "points": {
            (460, 150): [36, 217, 121],
            (460, 410): [36, 217, 121],
            (460, 670): [36, 217, 121],
            (180, 520): [80, 144, 255],
        },
        "sub_image_position": [382, 447, 654, 678],
        "expect_page_list": ["chose_support_card"],
    },
    "chose_support_card": {
        "points": {
            (240, 40): [73, 201, 73],
            (240, 480): [73, 201, 73],
            (790, 480): [162, 102, 255],
            (790, 660): [162, 102, 255],
        },
        "sub_image_position": [587, 645, 229, 260],
        "expect_page_list": ["cultivate_main"],
    },
    "cultivate_main": {
        "points": {
            (840, 600): [204, 187, 14],
            (840, 690): [204, 187, 14],
            (850, 600): [204, 187, 14],
            (850, 690): [204, 187, 14],
        },
        "sub_image_position": [560, 640, 957, 1037],
        "expect_page_list": ["train", "event", "match", "add_skill"],
    },
    "train": {
        "points": {
            (840, 600): [204, 187, 14],
            (840, 690): [204, 187, 14],
            (850, 600): [204, 187, 14],
            (850, 690): [204, 187, 14],
        },
        "sub_image_position": [56, 120, 1215, 1249],
        "expect_page_list": ["cultivate_main", "match", "event"],
    },
    "match": {
        "points": {
            (900, 600): [204, 187, 14],
            (900, 690): [204, 187, 14],
            (910, 600): [204, 187, 14],
            (910, 690): [204, 187, 14],
        },
        "sub_image_position": [155, 255, 1050, 1130],
        "expect_page_list": ["cultivate_main", "event"],
    },
    "event": {
        "points": {
            # 以下是2个选项时候第一个绿色
            (679, 360): [3, 206, 121],
            (680, 360): [65, 218, 154],
            (754, 360): [8, 207, 121],
            (755, 360): [8, 207, 121],
            # 以下是3个选项时候第一个绿色
            (567, 360): [3, 206, 121],
            (568, 360): [65, 218, 154],
            (642, 360): [8, 207, 121],
            (643, 360): [8, 207, 121],
            # 以下是5个选项时候第一个绿色
            (343, 360): [3, 206, 121],
            (344, 360): [65, 218, 154],
            (418, 360): [8, 207, 121],
            (419, 360): [8, 207, 121],
        },
        "sub_image_position": [29, 71, 0, 1280],
        "expect_page_list": ["cultivate_main"],
    },
    "toy_grab": {
        "points": {
            (62, 520): [22, 64, 121],
            (62, 500): [22, 64, 121],
            (198, 500): [22, 64, 121],
            (198, 520): [22, 64, 121],
        },
        "sub_image_position": [605, 655, 229, 260],
        "expect_page_list": ["cultivate_main"],
    },
    "cultivate_end": {
        "points": {
            (340, 356): [36, 217, 121],
            (610, 356): [36, 217, 121],
            (650, 356): [36, 217, 121],
            (730, 356): [36, 217, 121],
        },
        "sub_image_position": [445, 561, 1065, 1105],
        "expect_page_list": ["add_skill", "evolution_skill", "app_main"],
    },
    "add_skill": {
        "points": {
            (420, 300): [40, 211, 158],
            (420, 320): [40, 211, 158],
            (420, 440): [40, 211, 158],
            (420, 460): [40, 211, 158],
        },
        "sub_image_position": [600, 690, 300, 390],
        "expect_page_list": ["cultivate_end", "app_main"],
    },
    "evolution_skill": {
        "points": {
            (80, 200): [12, 197, 113],
            (80, 210): [12, 197, 113],
            (80, 520): [12, 197, 113],
            (80, 530): [12, 197, 113],
        },
        "sub_image_position": [163, 188, 1098, 1122],
        "expect_page_list": ["evolution_skill", "app_main"],
    },
    "pt_not_enough": {
        "points": {
            (435, 200): [12, 195, 107],
            (435, 210): [12, 195, 107],
            (435, 510): [12, 195, 107],
            (435, 520): [12, 195, 107],
        },
        "sub_image_position": [481, 556, 815, 854],
        "expect_page_list": ["app_main"],
    },
}

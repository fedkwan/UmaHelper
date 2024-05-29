data = {
    "app_main": {
        "point": {
            (1264, 300): (220, 130, 0),
            (1264, 360): (220, 130, 0),
            (1264, 420): (220, 130, 0),
            (920, 650): (102, 68, 221),
        },
        "sub_image_position": [220, 270, 1070, 1110],
        "expect_page_list": ["chose_scenario"],
    },
    "chose_scenario": {
        "point": {
            (260, 630): (64, 31, 88),
            (300, 630): (65, 32, 85),
            (300, 630): (67, 34, 90),
            (300, 630): (66, 33, 89),
        },
        "sub_image_position": [527, 620, 127, 157],
        "expect_page_list": ["chose_uma"],
    },
    "chose_uma": {
        "point": {
            (460, 150): (36, 217, 121),
            (460, 410): (36, 217, 121),
            (460, 670): (36, 217, 121),
            (367, 64): (34, 204, 255),
        },
        "sub_image_position": [470, 563, 402, 432],
        "expect_page_list": ["chose_parent_uma"],
    },
    "chose_parent_uma": {
        "point": {
            (460, 150): (36, 217, 121),
            (460, 410): (36, 217, 121),
            (460, 670): (36, 217, 121),
            (180, 520): (80, 144, 255),
        },
        "sub_image_position": [382, 447, 654, 678],
        "expect_page_list": ["chose_parent_uma"],
    },
    "chose_parent_uma_1": {},
    "chose_parent_uma_2": {},
    "chose_support_card": {
        "point": ["", "", "", ""],
        "sub_image_position": [],
        "expect_page_list": [],
    },
    "chose_support_card_detail": {
        "point": ["", "", "", ""],
        "sub_image_position": [],
        "expect_page_list": [],
    },
    "main": {
        "point": {
            (840, 600): (204, 187, 14),
            (840, 600): (204, 187, 14),
            (850, 690): (204, 187, 14),
            (850, 690): (204, 187, 14),
        },
        "sub_image_position": [957, 1037, 560, 64],
        "expect_page_list": ["train", "match_list", "skill"],
    },
    "train": {
        "point": {
            (840, 600): (204, 187, 14),
            (840, 600): (204, 187, 14),
            (850, 690): (204, 187, 14),
            (850, 690): (204, 187, 14),
        },
        "sub_image_position": [1215, 1249, 56, 120],
        "expect_page_list": ["main", "event"],
    },
    "event": {},
    "match": {
        "point": {
            (840, 600): (204, 187, 14),
            (840, 600): (204, 187, 14),
            (850, 690): (204, 187, 14),
            (850, 690): (204, 187, 14),
        },
    },
    "match_list": {
        "point": {
            (580, 36): (134, 126, 255),
            (560, 36): (134, 126, 255),
            (480, 670): (15, 66, 117),
            (490, 670): (15, 66, 117),
        },
        "sub_image_position": [1063, 1101, 101, 178],
        "expect_page_list": ["main", "find_cansai"],
    },
    "match_pre": {
        "point": {},
        "sub_image_position": [],
        "expect_page_list": ["match_result", "match_running_style" "match_inside"],
    },
    "match_result": {"waitfortap": 1},
    "match_result_ranking": {"continue"},
    "match_result_bonus": {"continue_icon", "main"},
    "cultivate_end": {
        "point": {
            (340, 356): (36, 217, 121),
            (610, 356): (36, 217, 121),
            (650, 356): (36, 217, 121),
            (730, 356): (36, 217, 121),
        },
        "sub_image_position": [445, 561, 1065, 1105],
        "expect_page_list": [""],
    },
}

from module.cultivate.skill_dic import *


def transform_dict(input_dict):
    # 创建一个新的字典以避免在迭代时修改原字典
    transformed_dict = {}
    for key, value in input_dict.items():
        # 将键与值转换为字符串后拼接
        transformed_dict[key] = f"{key}{value}"
    return transformed_dict


# 调用函数并输出结果
# transformed_dict = transform_dict(skill_dic_prototype)
# print(transformed_dict)

def create_inverse_mapping(dictionary):
    inverse_dict = {value: key for key, value in dictionary.items()}
    return inverse_dict


inverse_dict = create_inverse_mapping(skill_dic_combine_name_and_description)
print(inverse_dict)

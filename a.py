from collections import Counter

# 读取 TXT 文件内容
with open('find_list.txt', 'r', encoding='utf-8') as file:
    strings = file.readlines()

# 去除每行末尾的换行符
strings = [s.strip() for s in strings]

# 使用 Counter 统计每个字符串出现的次数
string_counts = Counter(strings)

# 将统计结果转换为字典
string_counts_dic = dict(string_counts)

# 输出结果
print(string_counts_dic)
from simhash import Simhash
import Levenshtein

def str_similarity(str1, str2):
    '''
    hash1 = Simhash(str1)
    hash2 = Simhash(str2)
    max_hash_bits = max(len(bin(hash1.value)), len(bin(hash2.value))) - 2
    hamming_distance = hash1.distance(hash2)
    similarity = 1 - (hamming_distance / max_hash_bits)
    '''
    distance = Levenshtein.distance(str1, str2)
    max_len = max(len(str1), len(str2))
    similarity = 1 - distance / max_len
    return similarity


def find_most_similar_string(target_str, str_dic):
    max_similarity = -1
    most_similar_str = None
    for k, v in str_dic.items():
        similarity = str_similarity(target_str, v)
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_str = v
    return most_similar_str


# test
if __name__ == "__main__":
    # 示例字符串数组和目标字符串
    _str_dic = {"你好2": "世界", "你好3": "世间", "再见": "世界", "你好": "朋友"}
    _target_str = "你好，宇宙"

    # 找到最相似的字符串
    _most_similar_str, _similarity = find_most_similar_string(_target_str, _str_dic)
    print(f"最相似的字符串: {_most_similar_str}")
    print(f"相似度: {_similarity}")

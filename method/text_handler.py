import Levenshtein


class TextHandler:

    @staticmethod
    def count_str_similarity(str1: str, str2: str) -> float:
        distance = Levenshtein.distance(str1, str2)
        max_len = max(len(str1), len(str2))
        similarity = 1 - distance / max_len
        return similarity

    def find_most_similar_str(self, target_str: str, str_dic: dict) -> str:
        max_similarity = -1
        most_similar_str = None
        for k, v in str_dic.items():
            similarity = self.count_str_similarity(target_str, v)
            if similarity > max_similarity:
                max_similarity = similarity
                most_similar_str = v
        return most_similar_str


# test
if __name__ == "__main__":

    _str_dic = {"你好2": "世界", "你好3": "世间", "再见": "世界", "你好": "朋友"}
    _target_str = "你好，宇宙"

    _handler = TextHandler()
    _a = _handler.find_most_similar_str(_target_str, _str_dic)

    print(_a)

import os
import re
import numpy as np


def find_numbers_in_string(string, model="stable"):
    numbers = re.findall(r'\d+', string)
    if not numbers:
        if model == "stable":
            return None
        elif model == "rude":
            return 0
    return int(''.join(numbers))


def get_png_files(folder):
    png_files = []
    files = os.listdir(folder)
    for file in files:
        if file.endswith(".png"):
            png_files.append(file)
    return png_files


# test
if __name__ == "__main__":
    print("x")

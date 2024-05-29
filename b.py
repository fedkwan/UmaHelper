from setting.base import *


def get_png_files(folder):
    png_files = []
    files = os.listdir(folder)
    for file in files:
        if file.endswith(".png"):
            png_files.append(file)
    return png_files

li = get_png_files(ROOT_DIR + "/resource/competition/c/")

print(li)
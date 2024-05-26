import uiautomator2 as u2
import psutil
import subprocess
from method.image_handler import *
from method.utils import *


def is_process_running(process_name):
    for process in psutil.process_iter(['name']):
        if process.info['name'] == process_name:
            return True
    return False


def start_process(process_path):
    try:
        subprocess.Popen(process_path)
        print(f"启动 {process_path} 成功。")
    except Exception as e:
        print(f"启动 {process_path} 失败: {e}")


def is_app_running(d, app_package):
    for app in d.app_list_running():
        if app == app_package:
            return True
    return False


process_name = "MuMuPlayer.exe"  # 替换为目标软件的进程名

a, b = 0, 0
while a == 0:
    if is_process_running(process_name):
        print(f"{process_name} 已经在运行。")
        ps_command = 'adb connect 127.0.0.1:16384'
        result = subprocess.run(["powershell", ps_command], capture_output=True, text=True, encoding='utf-8')
        print("输出:", result.stdout)
        print("错误:", result.stderr)
        if result.returncode == 0:
            print("cmd命令执行成功")
            d = u2.connect("127.0.0.1:16384")
            app_package = "com.komoe.kmumamusumegp"
            if is_app_running(d, app_package):
                print(f"手机APP： {app_package} 已经在运行。")
                d.app_stop(app_package)
                time.sleep(2)
                d.app_start(app_package)
                while b == 0:
                    screen = d.screenshot(format="opencv")
                    if np.all(screen[1261, 360] == np.array([247, 159, 28])):
                        a, b = 1, 1
                    resource_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/resource/"
                    part_image_file_li = get_png_files(resource_dir + "/start")
                    for part_image_file in part_image_file_li:
                        part_image = cv2.imread(resource_dir + "/start/" + part_image_file)
                        matcher = ImageMatcher(part_image, screen)
                        match_result = matcher.find_part_image_from_total_image()
                        if match_result is not None:
                            point = match_result["result"]
                            d.click(point[0], point[1])
                            time.sleep(DEFAULT_SLEEP_TIME)
                            continue
                    time.sleep(5)
            else:
                print(f"手机APP： {app_package} 没有在运行，正在尝试启动...")
                d.app_start(app_package)
        else:
            print("cmd命令执行失败")
    else:
        print(f"{process_name} 没有在运行，正先启动...")
    time.sleep(5)

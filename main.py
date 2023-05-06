import os
import subprocess
import sys
import time
import cv2
import numpy as np


# 使用adb截图
def adb_image():
    subprocess.call("adb shell screencap -p /sdcard/screen.png", shell=True, stdout=subprocess.DEVNULL)
    subprocess.call("adb pull /sdcard/screen.png ./img/screen.png", shell=True, stdout=subprocess.DEVNULL)
    

# 图像识别并点击
def match_image(template_file, num, cold):
    while True:
        # 加载图像
        adb_image()
        img_rgb = cv2.imread('./img/screen.png')
        img_template = cv2.imread('./img/' + template_file + '/' + str(num) + '.png')
        w, h = img_template.shape[:-1]

        # 使用OpenCV进行模板匹配
        result = cv2.matchTemplate(img_rgb, img_template, cv2.TM_CCOEFF_NORMED)

        # 匹配图像的坐标
        loc = np.where(result >= 0.8)

        if len(loc[0]) > 0:
            # 计算匹配图像的中心点
            center = (loc[1][0] + w // 2, loc[0][0] + h // 2)
            print("\033[32m" + "找到匹配图像，中心点坐标为：" + "\033[0m", center)
            sys.stdout.write("\033[F")  # 光标上移一行
            sys.stdout.write("\033[K")  # 清除当前行
            # 模拟点击
            subprocess.call("adb shell input tap {} {}".format(center[0], center[1]), shell=True, stdout=subprocess.DEVNULL)
            break
        else:
            print("\033[31m" + f"未找到匹配图像，{cold} 秒后重新查找" + "\033[0m")
            sys.stdout.write("\033[F")  # 光标上移一行
            sys.stdout.write("\033[K")  # 清除当前行
            time.sleep(cold)


# 加载上场角色池，关卡图
def rename_files(path):
    # 获取所有文件名
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    # 对文件名进行重命名，后缀名为txt，因为直接重命名可能会导致文件名重复而报错
    for i, file in enumerate(files):
        os.rename(os.path.join(path, file), os.path.join(path, str(i) + '.txt'))

    # 获取所有文件名
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    # 将文件后缀名命名回png
    for i, file in enumerate(files):
        os.rename(os.path.join(path, file), os.path.join(path, str(i) + '.png'))

    # 返回文件数量
    return len(files)

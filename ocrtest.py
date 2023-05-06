import pytesseract
from PIL import Image
import subprocess

# 使用adb截图
subprocess.call("adb shell screencap -p /storage/emulated/0/termux/github/AutoTouHouLostWordTermux/img/screen.png", shell=True, stdout=subprocess.DEVNULL)

# 读取图片文件
img = Image.open("./img/screen.png")

# 设置tesseract命令行参数
config = "-l chi_sim --oem 1 --psm 3"

# 调用image_to_data方法，返回一个字典列表
data = pytesseract.image_to_data(img, config=config, output_type=pytesseract.Output.DICT)

# 遍历字典列表，打印每个单词的文本和坐标
for i in range(len(data["text"])):
    word = data["text"][i]
    x = data["left"][i]
    y = data["top"][i]
    w = data["width"][i]
    h = data["height"][i]
    print(f"{word}: ({x}, {y}, {w}, {h})")

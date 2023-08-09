import cv2
import numpy as np

# 读取二值图像
image = cv2.imread('1.png', cv2.IMREAD_GRAYSCALE)

# 确保成功读取图像
if image is not None:
    # 二值化图像
    ret, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

    # 查找轮廓
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 找到最大轮廓
    max_contour = max(contours, key=cv2.contourArea)

    # 获取最小包围矩形
    rect = cv2.minAreaRect(max_contour)
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    # 计算相对坐标和类别
    width, height = image.shape[::-1]
    x, y, w, h = cv2.boundingRect(max_contour)
    relative_x = (x + w / 2) / width
    relative_y = (y + h / 2) / height
    relative_w = w / width
    relative_h = h / height
    class_label = 0  # 假设类别为0

    # 输出符合YOLOv5训练数据格式的位置信息
    print(f"{class_label} {relative_x} {relative_y} {relative_w} {relative_h}")
else:
    print("无法读取图像文件。")
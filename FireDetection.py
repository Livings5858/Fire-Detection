import cv2
import numpy as np

def detect_fire(image_path, area_threshold=500, circularity_threshold=0.5):
    # 定义火焰颜色的范围（HSV颜色空间）
    lower_bound = np.array([0, 200, 200])
    upper_bound = np.array([15, 255, 255])

    # 读取图片
    frame = cv2.imread(image_path)

    if frame is None:
        print("Error: Could not read image." + image_path)
        return False

    # 将图像从BGR转换为HSV颜色空间
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 使用颜色阈值检测火焰区域
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # 通过膨胀和腐蚀去除噪声
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # 查找轮廓
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # 计算轮廓的面积
        area = cv2.contourArea(contour)
        if area < area_threshold:
            continue

        # 如果满足面积和形状条件，则检测到火焰
        return True

    # 如果没有找到符合条件的火焰，返回False
    return False

# 使用示例
# image_path = 'nofire2.png'  # 替换为你的图片路径
# if detect_fire(image_path):
#     print("Fire detected!")
# else:
#     print("No fire detected.")

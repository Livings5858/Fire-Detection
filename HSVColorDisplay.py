import cv2
import numpy as np

def hsv_gradient_image(hsv_start, hsv_end, width=600, height=100):
    """
    创建一个从hsv_start到hsv_end的HSV颜色渐变图像。

    :param hsv_start: 起始HSV值 (h, s, v)
    :param hsv_end: 结束HSV值 (h, s, v)
    :param width: 图像宽度
    :param height: 图像高度
    :return: BGR图像
    """
    # 创建一个空白图像
    gradient_image = np.zeros((height, width, 3), dtype=np.uint8)

    # 生成HSV渐变
    for x in range(width):
        # 计算当前像素的HSV值
        t = x / (width - 1)  # 从0到1的归一化值
        h = int(hsv_start[0] * (1 - t) + hsv_end[0] * t)
        s = int(hsv_start[1] * (1 - t) + hsv_end[1] * t)
        v = int(hsv_start[2] * (1 - t) + hsv_end[2] * t)
        
        # 设置当前像素的HSV值
        gradient_image[:, x] = [h, s, v]

    # 将HSV图像转换为BGR图像
    bgr_image = cv2.cvtColor(gradient_image, cv2.COLOR_HSV2BGR)
    
    return bgr_image

def display_gradient(hsv_start, hsv_end):
    # 获取渐变图像
    gradient_image = hsv_gradient_image(hsv_start, hsv_end)
    
    # 显示图像
    cv2.imshow(f'HSV Gradient from {hsv_start} to {hsv_end}', gradient_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 示例HSV范围（H: 0-15, S: 200-255, V:200-255）
hsv_start = (0, 200, 200)  # 红色
hsv_end = (15, 255, 255)   # 黄色

display_gradient(hsv_start, hsv_end)

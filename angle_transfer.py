import cv2
import numpy as np


def image_padded(image):
    img_matrix = np.array(image)
    width = cv2.getOptimalDFTSize(np.size(img_matrix, 1))
    height = cv2.getOptimalDFTSize(np.size(img_matrix, 0))
    top_bottom = height - np.size(img_matrix, 0)
    left_right = width - np.size(img_matrix, 1)
    new_matrix = cv2.copyMakeBorder(img_matrix, 0, top_bottom,
                                    0, left_right, borderType=cv2.BORDER_CONSTANT,
                                    value=0)
    return new_matrix


def image_dft(image):
    temp_matrix = np.array(image)
    # 傅里叶变换
    forier_matrix = np.fft.fft2(temp_matrix)
    forier_matrix_shift = np.fft.fftshift(forier_matrix)
    forier_matrix_magnitude = np.log(np.abs(forier_matrix_shift))
    # 二值化
    forier_matrix_magnitude = forier_matrix_magnitude.astype(np.uint8)
    ret, threshold_matrix = cv2.threshold(forier_matrix_magnitude, 11, 255, cv2.THRESH_BINARY)   #  11这个阈值 可能需要根据情况变换
    cv2.imshow("wwq", threshold_matrix)
    # 霍夫直线变换
    lines = cv2.HoughLinesP(threshold_matrix, 2, np.pi/180, 30, minLineLength=0, maxLineGap=100)
    print(lines)
    return lines


def calculate_angle(lines, image):
    height, width = image.shape[:2]
    angle = 0.0
    piThresh = np.pi/90
    pi2 = np.pi/2
    for line in lines:
        x1, y1, x2, y2 = line[0]
        theta = abs(np.arctan2(y2 - y1, x2 - x1))   # 如果不是绝对值  有可能angle是负的  即 p2 比 p1 小
        lines_direction = np.arctan2(y2 - y1, x2 - x1)
        if abs(theta) < piThresh or abs(theta - pi2) < piThresh:
            continue
        else:
            angle = theta
            break
    if angle >= pi2:
        angle = angle - np.pi
    if angle != pi2:
        anglet = width * np.tan(angle) / height
        angle = np.arctan(anglet)
    angle = angle * (180 / np.pi)
    if lines_direction > 0:    # 方向判断，还需要改进一下
        angle = angle - 90
    else:
        angle = 90 - angle
    return angle


def image_rotated(angle, image):
    height, width = image.shape[:2]
    img_matrix = np.array(image)
    center = (width//2, height//2)
    temp_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_matrix = cv2.warpAffine(img_matrix, temp_matrix, (width, height), flags=cv2.INTER_CUBIC,
                                    borderMode=cv2.BORDER_REPLICATE)
    return rotated_matrix


if __name__ == '__main__':
    img = cv2.imread('E:/fuliye/imageText_05_R.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    padded_matrix = image_padded(gray)
    hough_lines = image_dft(padded_matrix)
    des_angle = calculate_angle(hough_lines, img)
    result_image = image_rotated(des_angle, img)
    cv2.imshow('current_image', img)
    cv2.imshow('des_image', result_image)
    # cv2.imwrite("E:/fqq.png", result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# -*- coding: utf-8 -*-
import cv2
import numpy as np


# 计算横向或者竖向每列非白像素的个数，image:传入的图像; direction：0->列，1->行
def calculate_pixel(image, direction):
    img_matrix = np.array(image)
    img_matrix = np.floor(img_matrix/255)
    img_matrix = np.logical_not(img_matrix)
    img_matrix = img_matrix+0
    pixel_sum = np.sum(img_matrix, axis=direction)
    return pixel_sum


# 根据传入的参数，生成固定大小的初始值为0的矩阵，dimension:拼接的矩阵的长或者宽维度;direction：0->列，1->行
def generate_matrix(dimension, direction):
    matrix = []
    if direction == 0:
        matrix = np.zeros((dimension+50, 50))   # 每行
    elif direction == 1:
        matrix = np.zeros((50, dimension))   # 每列
    matrix = np.add(matrix, 255)
    return matrix


# 将空矩阵填充起来,image:传入的图像;pix_sum:每列或者每行的非白像素个数之和;direction：0->列，1->行
def fill_matrix(image, pix_sum, direction):
    img_matrix = np.array(image)
    num = np.size(img_matrix, direction)
    temp_matrix = generate_matrix(num, direction)
    pix_sum_norm = np.floor(pix_sum/max(pix_sum)*50) # 归一化到50
    for i in range(num):   # 填充
        if pix_sum[i] != 0:
            for j in range(int(pix_sum_norm[i])):
                if direction == 1:
                    temp_matrix[49-j, i] = 0
                elif direction == 0:
                    temp_matrix[i, 49-j] = 0
    return temp_matrix


# 将矩阵拼接起来
def image_merge(image, col_pix, row_pix):
    img_matrix = np.array(image)
    ho_matrix = fill_matrix(image, col_pix, 1)
    ve_matrix = fill_matrix(image, row_pix, 0)
    img_matrix = np.vstack((img_matrix, ho_matrix))
    img_matrix = np.hstack((img_matrix, ve_matrix))
    return img_matrix


# 读取图片: cv2.imread(路径,num) 其中num=0，为灰度图像；num=1为彩图
img = cv2.imread('E:/tt.png', 0)
# 计算每列的非白像素求和
per_col = calculate_pixel(img, 0)
# 计算每行的非白像素求和
per_row = calculate_pixel(img, 1)
# 获得结果矩阵
result_matrix = image_merge(img, per_col, per_row)
cv2.imshow('result_image', result_matrix)
cv2.waitKey(0)
cv2.destroyAllWindows()
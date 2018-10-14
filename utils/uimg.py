import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


def save(file_path: str, img):
    """
    Do not use `cv2.imwrite` to save image, doesn't work as expected when it comes to Chinese file name
    :param file_path:
    :param img:
    :return:
    """
    cv.imencode('.jpg', img)[1].tofile(file_path)


def read(file_path: str):
    return cv.imdecode(np.fromfile(file_path, dtype=np.uint8), 0)


def show(img):
    plt.imshow(img, cmap='gray', interpolation='bicubic')
    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    plt.show()


def reverse(img):
    """
    :param img: channels = 1, dtype = numpy.uint8
    :return: val = 255 - val, pixel-wise
    """
    img = 255 - img
    return img

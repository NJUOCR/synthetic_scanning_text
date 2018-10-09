import random as rd
import numpy as np
import cv2 as cv


class Interference:

    def interfere(self, img):
        raise Exception("interfere function not implement")

    @staticmethod
    def get_bounds(img):
        """
        Get the minimum rectangle box containing the text. This method assumes that:
            1. there is no noise in the given image
            2. background color is white(255)
        :param img: input image
        :return: top, left, bottom, right
        > FYI: image_height = bottom - top, image_width = right - left
        """
        h, w = img.shape
        white_line = np.ones((h,), float) * 255
        for left in range(w):
            if not (img[:, left] == white_line).all():
                break
        else:
            left = None

        for right in range(w-1, -1, -1):
            if not (img[:, right] == white_line).all():
                break
        else:
            right = None

        for top in range(h):
            if not (img[top, :] == white_line).all():
                break
        else:
            top = None

        for bottom in range(h-1, -1, -1):
            if not (img[bottom, :] == white_line).all():
                break
        else:
            bottom = None

        return top, left, bottom, right

    @staticmethod
    def make_grid(img, x_num: tuple, y_num: tuple) -> list:
        """
        ***Ignore***
        :param img: input image
        :param x_num: (min_num, max_num) along width, border contained
        :param y_num: (min_num, max_num) along height, border contained
        :return: a list containing `x_num` x `y_num` cells
        """
        #获取图片的高和宽
        height, width = img.shape
        x = rd.randint(*x_num)
        y = rd.randint(*y_num)
        dx = width // x
        dy = height // y
        grids = []
        for i in range(y):
            for j in range(x):
                grids.append(img[i * dy:(i + 1) * dy, j * dx:(j + 1) * dx])
        return grids


class GaussianBlur(Interference):

    def __init__(self, r, sigma):
        """
        Gaussian blur with radius `r` and deviation `sigma`
        :param r: radius
        :param sigma: deviation
        """
        self.r = r
        self.sigma = sigma

    def interfere(self, img):
        return cv.GaussianBlur(img, (self.r, self.r), self.sigma)


class RandomTranslate(Interference):

    def __init__(self):
        """
        Randomly move the content(text) of the image, along both x and y axises.
        **Keep text in image boundary**
        """
        # todo cur_img?


    def interfere(self, img):
        # todo 随机平移
        #获取图片大小
        height, width = self.size()
        left, right, top, bottom = self.get_valid_rect()
        return img

    def get_valid_rect(self, img):
        left_bounding = 0
        ##?
        right_bounding = img.shape[1]

class RandomNoise(Interference):

    def __init__(self, p, min_brightness, max_brightness):
        """
        Add noise to image, every pixel in the image can be a noise pixel under the possibility `p`,
        the brightness of the noise pixel is between `min_brightness` and `max_brightness`

        > Background noise or foreground noise is decided by the brightness
        :param p: The possibility that one pixel in image is a noise pixel
        :param min_brightness: the minimum brightness of a noise
        :param max_brightness: the maximum brightness of a noise
        """
        self.p = p
        self.min_brightness = min_brightness
        self.max_brightness = max_brightness

    def interfere(self, img):
        # todo 增加噪点
        return img


class RandomResize(Interference):

    def __init__(self, min_scale, max_scale):
        """
        Resize image with a scale between `min_scale` and `max_scale`
        :param min_scale: should be larger than 0.0
        :param max_scale: should be smaller than or equal to 1.0
        """
        pass

    def interfere(self, img):
        # todo 缩放
        pass


class Padding(Interference):

    def __init__(self, width, height, val):
        """
        use `val` to pad the image to size of `width` x `height`
        :param width:
        :param height:
        :param val:
        """
        pass

    def interfere(self, img):
        # todo 边缘补齐
        pass


class RandomRotation(Interference):

    def __init__(self, min_angle, max_angle):
        """
        Rotate the image with a random angle between `min_angle` and `max_angle`
        :param min_angle: better use a value smaller than 0 to make a clockwise rotation
        :param max_angle: better use a value larger than 0 to make a anti-clockwise rotation
        """

    def interfere(self, img):
        # todo 旋转
        pass


class RandomDilution(Interference):

    def __init__(self, min_rate, max_rate):
        """
        Dilute the whole image by a random rate between `min_rate` and `max_rate`
        :param min_rate:
        :param max_rate:
        """

    def interfere(self, img):
        # todo 淡化
        pass

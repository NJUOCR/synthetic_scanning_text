import random as rd

import cv2 as cv
import numpy as np


class Interference:

    def interfere(self, img):
        """

        :param img:
        :return: A tuple (out_img, random_val)
        """
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
        black_vertical = np.zeros((h, ), np.uint8)
        black_horizontal = np.zeros((w, ), np.uint8)
        for left in range(w):
            if not (img[:, left] == black_vertical).all():
                break
        else:
            left = None

        for right in range(w - 1, -1, -1):
            if not (img[:, right] == black_vertical).all():
                break
        else:
            right = None

        for top in range(h):
            if not (img[top, :] == black_horizontal).all():
                break
        else:
            top = None

        for bottom in range(h - 1, -1, -1):
            if not (img[bottom, :] == black_horizontal).all():
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
        # 获取图片的高和宽
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


class Inversion(Interference):

    def __init__(self):
        """
        Inverse the input image
        """

    def interfere(self, img):
        """

        :param img: the input image, of which the mode should be `gray-scale`. An auto conversion will be
        done otherwise.
        :return: A gray-scale image
        """
        channel = img.shape[2] if len(img.shape) == 3 else 1
        # 颜色空间转换函数
        out = img
        if channel == 3:
            out = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        return 255 - out, None


class RandomGaussianBlur(Interference):

    def __init__(self, min_r, max_r, min_sigma, max_sigma):
        """
        Gaussian blur with random radius [min_r, max_r] and random sigma [min_sigma, max_sigma]
        :param min_r: minimum radius
        :param max_r: maximum radius
        :param min_sigma: minimum sigma
        :param max_sigma: maximum sigma
        """
        self.r_seeds = []
        for r in range(min_r, max_r+1, 2):
            self.r_seeds.append(r)
        self.sigma_range = max_sigma - min_sigma
        self.sigma_bias = min_sigma

    def interfere(self, img):
        r = self.r_seeds[rd.randint(0, len(self.r_seeds)-1)]
        sigma = rd.random() * self.sigma_range + self.sigma_bias
        return cv.GaussianBlur(img, (r, r), sigma), None


class RandomTranslation(Interference):

    def __init__(self):
        """
        Randomly move the content(text) of the image, along both x and y axises.
        **Keep text in image boundary**
        """

    def interfere(self, img):
        # 获取图片大小
        img_input = img
        height, width = img.shape
        top, left, bottom, right = Interference.get_bounds(img)

        if None in (top, left, bottom, right):
            return img_input, (0, 0)

        offset_x = rd.randint(-left, width - right)
        offset_y = rd.randint(-top, height - bottom)
        # 仿射矩阵，移位矩阵
        mat_translation = np.float32([[1, 0, offset_x],
                                      [0, 1, offset_y]])
        # 调用的一个仿射方法
        img_output = cv.warpAffine(img_input, mat_translation, (img_input.shape[1], img_input.shape[0]))
        return img_output, (offset_x, offset_y)


class RandomNoise(Interference):

    def __init__(self, rate, min_val, max_val):
        """
        Add noise to image, every pixel in the image can be a noise pixel under the possibility `p`,
        the val of the noise pixel is between `min_val` and `max_val`

        > Background noise or foreground noise is decided by the val
        :param rate: The possibility that one pixel in image is a noise pixel
        :param min_val: the minimum val of a noise
        :param max_val: the maximum val of a noise
        """
        self.rate = rate
        self.min_val = min_val
        self.max_val = max_val

    def interfere(self, img):
        # todo 增加噪点
        # white_noise
        w_rate = self.rate
        w_range = (self.max_val, self.max_val)
        # np.nditer: numpy array自带的迭代器 参考网址：https://www.jianshu.com/p/f2bd63766204
        # 按顺序遍历会出现噪点扎堆的请看
        for x in np.nditer(img, op_flags=['readwrite']):
            if rd.random() < w_rate:
                x[...] = rd.randint(*w_range)
        return img, None


class RandomResize(Interference):

    def __init__(self, min_scale, max_scale):
        """
        Resize image with a scale between `min_scale` and `max_scale`
        :param min_scale: should be larger than 0.0
        :param max_scale: should be smaller than or equal to 1.0
        """
        self.min_scale = min_scale
        self.max_scale = max_scale

    def interfere(self, img):
        # 生成min_scale至max_scale之间的随机浮点数
        scale = rd.uniform(self.min_scale, self.max_scale)
        height, width = img.shape
        # CV_INTER_LINEAR ：雙線性插補(預設)
        interpolation = cv.INTER_LINEAR
        # interpolation：內插方式
        img = cv.resize(img, (int(width * scale), int(height * scale)), interpolation=interpolation)
        return img, scale


class Padding(Interference):

    def __init__(self, width, height, val):
        """
        use `val` to pad the image to size of `width` x `height`
        :param width:
        :param height:
        :param val:
        """
        # 新的图片的宽度，高度
        self.width = width
        self.height = height
        self.val = val

    def interfere(self, img):
        # todo 边缘补齐
        new_height, new_width = self.height, self.width
        top = left = bottom = right = 0
        # 获取当前图片的宽度，高度
        cur_height, cur_width = img.shape
        if new_height > cur_height:
            # 上下填充
            top = (new_height - cur_height) // 2
            bottom = new_height - cur_height - top
        if new_width > cur_width:
            # 左右填充
            left = (new_width - cur_width) // 2
            right = new_width - cur_width - left
        if top == 0 and bottom == 0 and left == 0 and right == 0:
            return img, None
        out = cv.copyMakeBorder(img, top, bottom, left,  right, cv.BORDER_CONSTANT, value=self.val)
        return out, None


class RandomRotation(Interference):

    def __init__(self, min_angle, max_angle):
        """
        Rotate the image with a random angle between `min_angle` and `max_angle`
        :param min_angle: better use a value smaller than 0 to make a clockwise rotation
        :param max_angle: better use a value larger than 0 to make a anti-clockwise rotation
        """
        self.min_angle = min_angle
        self.max_angle = max_angle

    def interfere(self, img):
        height, width = img.shape
        angle = rd.random() * (self.max_angle - self.min_angle) + self.min_angle
        mat = cv.getRotationMatrix2D((width / 2, height / 2), angle, 0.8)
        output_img = cv.warpAffine(img, mat, (width, height))
        return output_img, angle


class RandomDilution(Interference):

    def __init__(self, min_ratio, max_ratio):
        """
        Dilute the whole image by a random ratio between `min_ratio` and `max_ratio`
        :param min_ratio: <= 100
        :param max_ratio: <= 100
        """
        self.min_ratio = min_ratio
        self.max_ratio = max_ratio

    def interfere(self, img):
        # todo 淡化
        ratio = rd.randint(self.min_ratio, self.max_ratio) / 100
        img = img * ratio
        return img, ratio


class RandomStroke(Interference):

    def __init__(self, bolder: float, plain: float, kernel_size: int):
        self.kernel_size = kernel_size
        self.bolder = bolder
        self.plain = plain

    def interfere(self, img):
        # todo 笔画
        # 定义一个2*2的十字形结构
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (self.kernel_size, self.kernel_size))
        if rd.random() < self.bolder:
            output_img = cv.dilate(img, kernel)
        elif self.bolder < rd.random() < self.bolder + self.plain:
            output_img = cv.erode(img, kernel)
        else:
            output_img = np.copy(img)

        return output_img, None


class AutoBin(Interference):
    def __init__(self, block):
        self.block = block

    def interfere(self, img):
        """
        :param img:
        :return:
        """
        # 读取图像，并转为灰度图
        # img_grey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        # 自适应二值化
        img = img.astype(np.uint8)
        img_at_mean = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,
                                           cv.THRESH_BINARY, self.block, 0)
        return img_at_mean, None


class Threshold(Interference):
    def __init__(self, thresh):
        self.thresh = thresh

    def interfere(self, img):
        _, output_img = cv.threshold(img, self.thresh, 255, cv.THRESH_BINARY)
        return output_img, None
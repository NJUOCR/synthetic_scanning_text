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

    def interfere(self, img):
        # todo 随机平移
        #获取图片大小
        img_input = img
        height, width = self.size()
        left, right, top, bottom = self.get_valid_rect()
        offset_x = None
        offset_y = None
        offset_x = rd.randint(-left, width - right) if offset_x is None else rd.randint(-offset_x, offset_x)
        offset_y = rd.randint(-top, height - bottom) if offset_y is None else rd.randint(-offset_y, offset_y)
        #缩放矩阵？
        MatScale = np.float32([[1, 0, offset_x],
                        [0, 1, offset_y]])
        #调用的一个仿射方法
        img_output = cv.warpAffine(img_input, MatScale, (img_input.shape[1], img_input.shape[0]))
        return img_output

    def get_valid_rect(self, img):
        left_bounding = 0
        #宽度-1
        right_bounding = img.shape[1] - 1
        top_bounding = 0
        #高度-1
        bottom_bounding = img.shape[0] - 1

        left_found = False
        for i in range(0, right_bounding, 1):
            for px in self.cur_img[:, i]:
                if px > 0:
                    left_bounding = i
                    left_found = True
                    break
            if left_found:
                break

        right_found = False
        for i in range(right_bounding, -1, -1):
            for px in self.cur_img[:, i]:
                if px > 0:
                    right_bounding = i
                    right_found = True
                    break
            if right_found:
                break

        top_found = False
        for i in range(0, bottom_bounding, 1):
            for px in self.cur_img[i, :]:
                if px > 0:
                    top_bounding = i
                    top_found = True
                    break
            if top_found:
                break

        bottom_found = False
        for i in range(bottom_bounding, -1, -1):
            for px in self.cur_img[i, :]:
                if px > 0:
                    bottom_bounding = i
                    bottom_found = True
                    break
            if bottom_found:
                break

        return left_bounding, right_bounding, top_bounding, bottom_bounding


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
        # white_noise
        w_rate = 0.005
        w_range = (50, 110)
        # np.nditer: numpy array自带的迭代器 参考网址：https://www.jianshu.com/p/f2bd63766204
        for x in np.nditer(img, op_flags = ['readwrite']):
            if rd.random() < w_rate:
                x[...] = rd.randint(*w_range)
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
        scale = 1.0
        height, width = img.shape
        # CV_INTER_LINEAR ：雙線性插補(預設)
        interpolation = cv.INTER_LINEAR
        # interpolation：內插方式
        img = cv.resize(img, (int(width * scale), int(height *scale)), interpolation=interpolation)

        return img
        pass


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
        pass

    def interfere(self, img):
        # todo 边缘补齐
        new_height, new_width = self.height, self.width
        top =  left = bottom = right = 0
        # 获取当前图片的宽度，高度
        cur_height, cur_width = img.shape
        if new_height > cur_height:
            # 上下填充
            top = (new_height - cur_height) // 2
            bottom = new_height - cur_width - top
        if new_width > cur_width:
            # 左右填充
            left = (new_width - cur_width) // 2
            right = new_width - cur_width - left
        if top == 0 and bottom == 0 and left == 0 and right == 0:
            print("no need for padding")
            return
        img = cv.copyMakeBorder(img, top, bottom, left, right, cv.BORDER_CONSTANT, value=0)
        return img
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

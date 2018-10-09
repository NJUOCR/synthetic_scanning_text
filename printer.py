import numpy as np
from PIL import ImageFont


class Printer:

    def __init__(self, font_file: str, font_size: int):
        font = ImageFont.truetype(font_file, font_size)

    def print(self, width, height, text_gen: iter):
        """
        Print text on a `width` x `height` canvas
        :param width: the width of the canvas
        :param height: the height of the canvas
        :param text_gen: a generator which yield text to draw upon the canvas
        :return: A generator, yielding `image` and `text`(label)
        """
        for text in text_gen:
            img = np.ones((height, width), dtype=float) * 255
            # todo 在空白图片上写入文字
            yield img,  text

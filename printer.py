import re

import numpy as np
from PIL import ImageFont, ImageDraw, Image


class Printer:

    def __init__(self, font_file: str, font_size: int):
        self.font_size = font_size
        self.font = ImageFont.truetype(font_file, font_size)

    def print(self, width, height, text_gen: iter):
        """
        Print text on a `width` x `height` canvas
        :param width: the width of the canvas
        :param height: the height of the canvas
        :param text_gen: a generator which yield text to draw upon the canvas
        :return: A generator, yielding `image` and `text`(label)
        """
        for text, seq_len in text_gen:
            # 生成元素值为255的数组
            # img = np.ones((height, width), dtype=float) * 255
            # img = Image.new("1", (width, height), 1)

            # todo 在空白图片上写入文字
            # 生成空白图像,(宽度，高度 )
            img = Image.new("RGB", (width, height), color="white")
            # 绘图句柄
            draw = ImageDraw.Draw(img)
            font_width = font_height = self.font_size
            beginX, beginY = (10, 20)
            # 绘图
            draw.text((beginX, beginY), text, font=self.font, fill="black")

            '''
            padding_left = (width - seq_len * font_width) // 2
            print(padding_left)
            padding_top = (height - font_height) // 2
            draw.text((padding_left, padding_top), text, font=self.font)
            '''
            # yield ((np.array(img.getdata()).astype(float)) * 255).reshape(height, width), text
            yield ((np.array(img.getdata()).astype(np.uint8)) * 255).reshape(height, width), text

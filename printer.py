import numpy as np
from PIL import ImageFont, Image, ImageDraw

import re
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
            # 生成元素值为255的数组
            img = np.ones((height, width), dtype=float) * 255
            # todo 在空白图片上写入文字

            draw = ImageDraw.Draw(img)
            width, height = img.shape
            font_width, font_height = img.font_size
            # ?
            seq_len = len(text) - len(list(re.compile('\d|-').finditer(text)))/2
            if width < seq_len * font_width or height < font_height:
                print("text bigger than canvas: text => %s, canvas => (%d, %d), image => (%d, %d)" % (
                text, width, height, font_width * len(text), font_height))

            padding_left = (width - seq_len * font_width) // 2
            padding_top = (height - font_height) // 2
            draw.text((padding_left, padding_top), text, font = img.font)

            return ((np.array(img.getdata()).astype(float))*255).reshape(height,width)

            yield img,  text

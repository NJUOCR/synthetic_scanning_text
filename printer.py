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
            # 生成空白图像, (宽度，高度 )
            img = Image.new("1", (width, height), color="white")

            # 绘图句柄
            draw = ImageDraw.Draw(img)
            begin_x, begin_y = (10, 20)

            # 绘图
            draw.text((begin_x, begin_y), text, font=self.font, fill="black")
            im = (np.array(img.getdata()).astype(np.uint8)).reshape(height, width)
            yield im, text

import random as rd

import numpy as np

import utils.uimg as uimg
import utils.utility as util
from interference import RandomRotation
from printer import Printer


def init_img(font_path, min_font_size, max_font_size, canvas_width, canvas_height, txt_path, min_sen_len, max_sen_len):
    font_size = rd.randint(min_font_size, max_font_size)
    printer = Printer(font_path, font_size)
    img = printer.print_one(canvas_width, canvas_height, read_txt(txt_path, min_sen_len, max_sen_len))
    return img


# test read file
def read_txt(txt_path, min_sen_len, max_sen_len, space_frequency=0.3):
    # 句子长度
    sen_len = rd.randint(min_sen_len, max_sen_len)
    random_sen = ""
    # 把汉字输入进一个数组中
    words_list = []
    with open(txt_path, 'r', encoding='utf-8') as f:
        for line in f:
            words_list.append(line.strip())

    # 随机生成大小为sen_len大小的汉字数据
    for le in range(sen_len):
        r = rd.randint(0, len(words_list) - 1)
        char = words_list[r]
        space = " " if rd.random() < space_frequency else ""
        random_sen += (space + char)
    return random_sen


if __name__ == '__main__':
    config = util.read_config('config/template.json')
    ops = config['ops']
    file_index = rd.randint(0, len(config['font']['files']))

    for i in range(config['number']):
        original_im = init_img(config['font']['files'][file_index], config['font']['min_size'],
                               config['font']['max_size'], config['canvas']['width'], config['canvas']['height'],
                               config['char_path']['path'], config['char_path']['min_sen_len'],
                               config['char_path']['max_sen_len'])
        im = np.copy(original_im)
        angle = 0
        for op, p in ops:
            if rd.random() > p:
                continue
            im, val = op.interfere(im)
            if isinstance(op, RandomRotation):
                angle = val
        uimg.save("%s/%d_%.4f.jpg" % (config['out'], i, angle), uimg.reverse(im))

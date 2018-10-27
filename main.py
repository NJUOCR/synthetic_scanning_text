import random as rd

import numpy as np
from progressbar import ProgressBar

import utils.uimg as uimg
import utils.utility as util
from interference import RandomRotation
from printer import Printer


def init_printer(min_font_size, max_font_size, font_files: list) -> dict:
    """
    Generate `(max_font_size-min_font_size) * len(font_files)` `Printer` instances
    :param min_font_size:
    :param max_font_size:
    :param font_files: paths of font files
    :return: a `dict`, of which `key` is formed like `(font_file_path, font_size)`, indicating
    the corresponding Printer instance.
    """
    printer_dict = {}
    for font_size in range(min_font_size, max_font_size + 1):
        for font_file_idx, font_file in enumerate(font_files):
            printer_dict[(font_file_idx, font_size)] = Printer(font_file, font_size)
    return printer_dict


def init_img(font_path, min_font_size, max_font_size, canvas_width, canvas_height, txt_path, min_sen_len, max_sen_len):
    """
    Deprecated!
    :param font_path:
    :param min_font_size:
    :param max_font_size:
    :param canvas_width:
    :param canvas_height:
    :param txt_path:
    :param min_sen_len:
    :param max_sen_len:
    :return:
    """
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


def generate_rotation(config_file="config/rotation.json", char_file='text_seeds/char.txt', sen_len_range=(2, 10)):
    config = util.read_config(config_file)
    ops = config['ops']
    config_font = config['font']
    printer_dict = init_printer(config_font['min_size'], config_font['max_size'], config_font['files'])

    def get_random_printer():
        f_idx = rd.randint(0, len(config_font['files']) - 1)
        f_size = rd.randint(config_font['min_size'], config_font['max_size'])
        return printer_dict[(f_idx, f_size)]

    with ProgressBar(max_value=config['number']) as bar:
        for i in range(config['number']):
            printer = get_random_printer()
            text = read_txt(char_file, *sen_len_range)
            original_im = printer.print_one(config['canvas']['width'], config['canvas']['height'], text)
            im = np.copy(original_im)
            angle = 0
            for op, p in ops:
                if rd.random() > p:
                    continue
                im, val = op.interfere(im)
                if isinstance(op, RandomRotation):
                    angle = val
            uimg.save("%s/%d_%.4f.jpg" % (config['out'], i, angle), im)
            bar.update(i + 1)


def generate_single_char(config_file="config/single_char.json", char_file='text_seeds/char.txt'):
    config = util.read_config(config_file)
    ops = config['ops']
    config_font = config['font']
    printer_dict = init_printer(config_font['min_size'], config_font['max_size'], config_font['files'])

    def get_random_printer():
        f_idx = rd.randint(0, len(config_font['files']) - 1)
        f_size = rd.randint(config_font['min_size'], config_font['max_size'])
        return printer_dict[(f_idx, f_size)]

    with ProgressBar() as bar:
        with open(char_file, encoding='utf-8') as f:
            for i, line in enumerate(f):
                char = line.strip()
                for j in range(config['number']):
                    printer = get_random_printer()
                    original_im = printer.print_one(config['canvas']['width'],
                                                    config['canvas']['height'],
                                                    char)
                    im = np.copy(original_im)
                    for op, p in ops:
                        if rd.random() > p:
                            continue
                        im, val = op.interfere(im)
                    uimg.save("%s/%d_%s.jpg" % (config['out'], i * config['number'] + j, char), im)
                    bar.update(bar.value + 1)


if __name__ == '__main__':
    # generate_rotation()
    generate_single_char()

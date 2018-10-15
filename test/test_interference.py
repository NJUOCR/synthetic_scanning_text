from printer import Printer
from interference import RandomRotation
import utils.uimg as uimg
import utils.utility as util
import random as rd
import numpy as np

def init_img(font_path, min_font_size, max_font_size,  canvas_width, canvas_height, txt_path, sen_len):
    font_size = rd.randint(min_font_size, max_font_size)
    printer = Printer(font_path, font_size)
    img = printer.print_one(canvas_width, canvas_height, read_txt(txt_path, sen_len))
    return img

# test read file
def read_txt(txt_path, sen_len):
    # 句子长度
    # sen_len = 10
    random_sen = ""
    # 把汉字输入进一个数组中
    words_list = []
    with open(txt_path, 'r', encoding='utf-8') as f:
        data = f.readlines()  # txt中所有字符串读入data
        # print(data)
        for line in data:
            line = line.strip()
            word = line.split(" ")
            words_list = words_list + word
        # print(words_list)
    # 随机生成大小为sen_len大小的汉字数据
    for le in range(sen_len):
        r = rd.randint(0, words_list.__len__() - 1)
        te = words_list[r]
        random_sen = str(te) + random_sen
    return random_sen
    f.close()

if __name__ == '__main__':
    config = util.read_config('config/template.json')
    ops = config['ops']

    original_im = init_img(config['font']['files'][0], config['font']['min_size'], config['font']['max_size'], config['canvas']['width'], config['canvas']['height'], config['char_path']['path'], config['char_path']['sen_len'])

    for i in range(5):
        im = np.copy(original_im)
        angle = 0
        for op, p in ops:
            if rd.random() > p:
                continue
            rs = op.interfere(im)
            if rs is None:
                print("rs is None")
            im, val = rs
            if isinstance(op, RandomRotation):
                angle = val
        uimg.save("data/%d_%.4f.png" % (i, angle), uimg.reverse(im))
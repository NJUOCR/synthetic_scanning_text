import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


import json
import interference as itf


def read_config(config_file: str) -> dict:
    """
    Read config from `config_file`
    :param config_file: a config file indicate how to generate a batch of samples, it includes
    1. the orders to interfere the image, eg. `add_noise` -> `randomly_resize` -> `randomly_rotate`
    and so on.
    2. the total number of samples you want to generate
    3. the path you want to save the output samples
    4. other useful things
    :return: to be determined...
    """
    f = open(config_file, encoding='utf-8')
    config = json.load(f)
    f.close()

    ops = []
    for operation in config['interference_ops']:
        name = operation['name']
        opt = operation['opt']
        cls = None
        if name == 'random_stroke':
            cls = itf.RandomStroke(opt["bolder"], opt["plain"], 3)
        elif name == 'random_resize':
            cls = itf.RandomResize(opt['min_scale'], opt['max_scale'])
        elif name == 'random_rotation':
            cls = itf.RandomRotation(opt['min_angle'], opt['max_angle'])
        elif name == 'random_dilution':
            cls = itf.RandomDilution(opt['min_ratio'], opt['max_ratio'])
        elif name == 'padding':
            cls = itf.Padding(opt['width'], opt['height'], opt['val'])
        elif name == 'random_translation':
            cls = itf.RandomTranslation()
        elif name == 'random_noise':
            cls = itf.RandomNoise(opt['rate'], opt['min_val'], opt['max_val'])
        elif name == 'random_gaussian_blur':
            cls = itf.RandomGaussianBlur(opt['min_r'], opt['max_r'], opt['min_sigma'], opt['max_sigma'])

        if cls is not None:
            ops.append((cls, operation['p']))
    return {
        'ops': ops,
        'fonts': config['fonts']
    }


def save_sample(file_path: str, img):
    """
    Do not use `cv2.imwrite` to save image, doesn't work as expected when it comes to Chinese file name
    :param file_path:
    :param img:
    :return:
    """
    cv.imencode('.jpg', img)[1].tofile(file_path)

def read_img(file_path: str):
    return cv.imdecode(np.fromfile(file_path, dtype=np.uint8), 0)


def show_img(img):
    plt.imshow(img, cmap='gray', interpolation='bicubic')
    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    plt.show()
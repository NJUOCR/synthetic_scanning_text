import cv2 as cv


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
    pass


def save_sample(file_path: str, img):
    """
    Do not use `cv2.imwrite` to save image, doesn't work as expected when it comes to Chinese file name
    :param file_path:
    :param img:
    :return:
    """
    cv.imencode('.jpg', img)[1].tofile(file_path)
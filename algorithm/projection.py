"""
Please implement `projective histogram` here
"""
import Histogram_Generator as hg
import numpy as np


def project(img, direction='vertical'):
    """
    Do projection.
    :param img: A numpy array. source image.
    :param direction: `vertical` | `horizontal`
    :return: A numpy array with shape (1, )
    """
    dir = 0
    if direction == 'horizontal':
        dir = 1
    return hg.calculate_pixel(img, dir)


def draw_projective_histogram(img, direction='both'):
    """
    1. Copy the input img array
    2. Do padding, on right, bottom or both, according to the `direction`
    3. Draw histogram

    > The original input image will not be changed.
    :param img: A numpy array, the source image.
    :param direction: `vertical` | `horizontal` | `both`(default)
    :return: A numpy array
    """
    temp_matrix = np.array(img)
    per_col = project(temp_matrix, 'vertical')
    per_row = project(temp_matrix, 'horizontal')
    if direction == 'vertical':
        return hg.vertical_merge(temp_matrix, per_col)
    elif direction == 'horizontal':
        return hg.horizontal_merge(temp_matrix, per_row)
    else:
        horizontal_matrix = hg.horizontal_merge(temp_matrix, per_row)
        result_matrix = hg.vertical_merge(horizontal_matrix, per_col)
        return result_matrix

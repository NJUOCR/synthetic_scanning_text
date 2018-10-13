"""
Please implement `projective histogram` here
"""


def project(img, direction='vertical'):
    """
    Do projection.
    :param img: A numpy array. source image.
    :param direction: `vertical` | `horizontal`
    :return: A numpy array with shape (1, )
    """


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
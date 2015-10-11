import os


def window_height():
    return 420


def window_width():
    return 200


def num_rows():
    return 21


def num_columns():
    return 10


def font_path():
    return os.path.join(os.environ["windir"],"Fonts","Arial.ttf")

from settings import *


def rgb_to_hex(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'


def mapping(x, y):
    return (x // SQUARE_SIDE) * SQUARE_SIDE, (y // SQUARE_SIDE) * SQUARE_SIDE


def mini_mapping(x, y):
    return (x // MINI_MAP_SQUARE_SIDE) * MINI_MAP_SQUARE_SIDE,\
           (y // MINI_MAP_SQUARE_SIDE) * MINI_MAP_SQUARE_SIDE

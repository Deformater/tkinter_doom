from settings import *


MAP = [
    '||||||||||||',
    '|..........|',
    '|..........|',
    '|..........|',
    '|..........|',
    '||||||||||||'
]

world_map = set()

for i, row in enumerate(MAP):
    for j, wall in enumerate(row):
        if wall != '.':
            world_map.add((j * SQUARE_SIDE, i * SQUARE_SIDE))
